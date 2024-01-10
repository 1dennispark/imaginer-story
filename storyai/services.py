import io
import json
import logging
import uuid
from typing import BinaryIO

import httpx
import oci
import openai
import sqlalchemy as sa
import sqlalchemy.orm as orm
from oci.object_storage import ObjectStorageClient

from . import domain, completion, models
from .models import AddCharacterInput, Character, GenerateCharacterInput, GenerateCharacterOutput, \
    GenerateSynopsisInput, GenerateScenarioInput, SynopsisContent

logger = logging.getLogger(__name__)


def _character_prompt(name: str, mbti: str, age_range: str, gender: domain.Gender, description: str) -> str:
    return f"""# 페르소나
- 이름: "{name}"
- 성격 유형(MBTI): "{mbti}"
- 나이대: {age_range}
- 성별: "{gender}"
- 설명: "{description}"

위 페르소나를 보고 그에 어울리는 캐릭터의 특징을 자세하게 소개해줘."""


def _synopsis_prompt(
        character_1: domain.Persona,
        character_2: domain.Persona,
        genre: str,
        background: str,
        ending: str,
        event_description: str,
) -> str:
    return f"""# 캐릭터 소개
## {character_1.name}
- 성격 유형(MBTI): {character_1.mbti}
- 나이대: {character_1.age}
- 성별: {character_1.gender}
- 설명: {character_1.context}

## {character_2.name}
- 성격 유형(MBTI): {character_2.mbti}
- 나이대: {character_2.age}
- 성별: {character_2.gender}
- 설명: {character_2.context}

# 시놉시스 설명
- 장르: {genre}
- 배경: {background}
- 결말: {ending}
- 개요: {event_description}

""" + """# 포맷
```json
[{{"title": "..., "detail": ...}}, ...]
```

위 캐릭터 소개와 시놉시스 설명을 보고 "포맷"에 맞게 시놉시스를 3부작으로 만들어줘."""


def _scenario_prompt(
        character_1: domain.Persona,
        character_2: domain.Persona,
        genre: str,
        background: str,
        ending: str,
        event_description: str,
        synopses: list[SynopsisContent],
) -> str:
    scenario = '\n'.join([f"{i+1}장. {s.title}\n{s.detail}\n" for i, s in enumerate(synopses)])
    return f"""# 캐릭터 소개
## {character_1.name}
- 성격 유형(MBTI): {character_1.mbti}
- 나이대: {character_1.age}
- 성별: {character_1.gender}
- 설명: {character_1.description}

## {character_2.name}
- 성격 유형(MBTI): {character_2.mbti}
- 나이대: {character_2.age}
- 성별: {character_2.gender}
- 설명: {character_2.description}

# 시놉시스
- 장르: {genre}
- 배경: {background}
- 결말: {ending}
- 개요: {event_description}

# 시나리오
{scenario}

위의 시나리오를 대사로 만들어줘."""


class PersonaService:

    def __init__(
            self,
            db: orm.Session,
            completer: completion.Completer):
        self._completer = completer
        self._db = db

    def generate_character(self, input: GenerateCharacterInput) -> GenerateCharacterOutput:
        prompt = _character_prompt(
            input.name,
            input.mbti,
            input.age,
            input.gender,
            input.description,
        )

        context = self._completer.chat([{
            'role': 'user',
            'content': prompt,
        }])

        # TODO: generate image from dreambooth
        profile_image = input.original_images[0]

        return GenerateCharacterOutput(context=context, profile_image=profile_image)

    def add_character(
            self,
            input: AddCharacterInput,
    ) -> Character:
        persona = domain.Persona(
            name=input.name,
            mbti=input.mbti,
            age=input.age,
            gender=input.gender,
            description=input.description,
            context=input.context,
            original_images=input.original_images,
            profile_image=input.profile_image,
        )
        with self._db.begin():
            self._db.add(persona)

        return Character.model_validate(persona)

    def get_all_characters(self) -> list[Character]:
        stmt = sa.select(domain.Persona).order_by(domain.Persona.id.desc())
        personas = list(self._db.execute(stmt).scalars().all())

        return [Character.model_validate(persona) for persona in personas]

    def get_character(self, persona_id: int) -> Character:
        stmt = sa.select(domain.Persona).where(domain.Persona.id == persona_id).limit(1)
        persona = self._db.execute(stmt).scalar_one()

        return Character.model_validate(persona)


class SynopsisService:
    def __init__(
            self,
            db: orm.Session,
            completer: completion.Completer,
    ):
        self._completer = completer
        self._db = db

    def generate_scenario(
            self,
            input: GenerateScenarioInput,
    ) -> str:
        character_1, character_2 = self._db.execute(
            sa.select(domain.Persona).where(domain.Persona.id.in_(input.character_ids)).limit(2)
        ).scalars().all()

        chat = [{
            'role': 'user',
            'content': _scenario_prompt(
                character_1,
                character_2,
                input.genre,
                input.background,
                input.ending,
                input.event_description,
                input.synopses,
            ),
        }]

        content = self._completer.chat(chat)

        return content

    def generate_synopsis(
            self,
            input: GenerateSynopsisInput,
    ) -> list[dict[str, str]]:
        [character_1, character_2] = self._db.execute(
            sa.select(domain.Persona).where(domain.Persona.id.in_(input.character_ids)).limit(2)
        ).scalars().all()

        chat = [{
            'role': 'user',
            'content': _synopsis_prompt(
                character_1,
                character_2,
                input.genre,
                input.background,
                input.ending,
                input.event_description,
            ),
        }]

        contents = self._completer.chat(chat)
        logger.debug(f"first answer: {contents}")
        parsed = json.loads(contents)

        return parsed


class ImageStorageService:
    def __init__(
            self,
            client: ObjectStorageClient,
            namespace: str,
            bucket: str,
    ):
        self._client = client
        self._ns = namespace
        self._bucket = bucket
        self._prefix = 'images/'

    def store(self, body: BinaryIO, content_type: str, ext: str = '') -> (str, str):
        object_name = uuid.uuid4().hex

        if ext != '':
            object_name += ext

        resp = self._client.put_object(
            namespace_name=self._ns,
            bucket_name=self._bucket,
            object_name=self._prefix + object_name,
            put_object_body=body,
            content_type=content_type,
        )

        return object_name, resp.headers['etag']

    def load(self, object_name, etag: str = '') -> (httpx.Response | None, str|None, str | None):
        try:
            resp = self._client.get_object(
                namespace_name=self._ns,
                bucket_name=self._bucket,
                object_name=self._prefix + object_name,
                if_none_match=etag,
            )

            content_type = resp.headers['content-type']
            etag = resp.headers['etag']

            return resp.data, content_type, etag
        except oci.exceptions.ServiceError as e:
            if e.status == 304:
                return None, None, None
            raise

    def remove(self, object_name: str) -> None:
        resp = self._client.delete_object(
            namespace_name=self._ns,
            bucket_name=self._bucket,
            object_name=self._prefix + object_name,
        )

        resp.data.raise_for_status()

