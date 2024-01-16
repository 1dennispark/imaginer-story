import io

import logging
import sqlalchemy as sa
import sqlalchemy.orm as orm

from . import DreamBoothService, ImageStorageService
from .. import domain, completion, proto, models
from ..models import AddCharacterInput, Character

logger = logging.getLogger(__name__)


def _character_prompt(name: str, mbti: str, age_range: str, gender: domain.Gender, description: str) -> str:
    return f"""# 페르소나
- 이름: "{name}"
- 성격 유형(MBTI): "{mbti}"
- 나이대: {age_range}
- 성별: "{gender}"
- 설명: "{description}"

위 페르소나를 보고 그에 어울리는 캐릭터의 특징을 자세하게 소개해줘."""


class PersonaService:
    def __init__(
            self,
            db: orm.Session,
            completer: completion.Completer,
            dreambooth_service: DreamBoothService,
            storage_service: ImageStorageService,
    ):
        self._completer = completer
        self._db = db
        self._dreambooth_service = dreambooth_service
        self._storage_service = storage_service

    def save_character(self, id: int | None, input: AddCharacterInput) -> Character:
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

        booth_id = self._dreambooth_service.create_booth(input.original_images, input.gender)
        with self._db.begin():
            if id is not None:
                persona = self._db.get(domain.Persona, id)
                persona.name = input.name
                persona.mbti = input.mbti
                persona.age = input.age
                persona.gender = input.gender
                persona.job = input.job
                persona.description = input.description
                persona.context = context
                persona.original_images = input.original_images
                persona.booth_id = booth_id
                persona.profile_image = None
                self._db.merge(persona)
            else:
                persona = domain.Persona(
                    name=input.name,
                    mbti=input.mbti,
                    age=input.age,
                    gender=input.gender,
                    job=input.job,
                    description=input.description,
                    context=context,
                    original_images=input.original_images,
                    profile_image=None,
                    booth_id=booth_id,
                )
                self._db.add(persona)

        character = Character.model_validate(persona)
        character.profile_image = "loading"
        return character

    def get_all_characters(self) -> list[Character]:
        stmt = sa.select(domain.Persona).order_by(domain.Persona.id.desc())
        personas = list(self._db.execute(stmt).scalars().all())

        return [Character.model_validate(persona) for persona in personas]

    def get_character(self, persona_id: int) -> Character:
        with self._db.begin():
            stmt = sa.select(domain.Persona).where(domain.Persona.id == persona_id).limit(1)
            persona = self._db.execute(stmt).scalar_one()
            character = Character.model_validate(persona)
        return character

    def get_profile_image(self, persona_id: int) -> models.ProfileImage:
        with self._db.begin():
            stmt = sa.select(domain.Persona).where(domain.Persona.id == persona_id).limit(1)
            persona = self._db.execute(stmt).scalar_one()
            profile_image = persona.profile_image
            status = "ok"
            if profile_image is None:
                state, err = self._dreambooth_service.get_booth(persona.booth_id)
                if state == proto.READY or state == proto.TRAINING:
                    status = "loading"
                elif state == proto.FINISHED:
                    profile_image = self._diffuse_profile_image(persona.booth_id, persona.job, persona.gender)
                    persona.profile_image = profile_image
                    self._db.merge(persona)
                elif state == proto.ERRORED:
                    logger.error(RuntimeError(f"errored: {err}"))
                    status = "errored"
                else:
                    raise RuntimeError(f"Unknown state: {state}, error: {err}")

        return models.ProfileImage(object_name=profile_image, status=status)

    def _diffuse_profile_image(self, booth_id: int, job: str, gender: domain.Gender) -> str:
        image_content = self._dreambooth_service.diffuse_booth(booth_id, job, gender)
        object_name, _ = self._storage_service.store(io.BytesIO(image_content), "image/jpeg", '.jpg')
        return object_name
