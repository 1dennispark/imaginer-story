import json
import logging
import sqlalchemy as sa
import sqlalchemy.orm as orm

from .. import domain, completion
from ..models import GenerateSynopsisInput, GenerateScenarioInput, SynopsisContent

logger = logging.getLogger(__name__)


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

위 캐릭터 소개와 시놉시스 설명을 보고 "포맷"에 맞게 시놉시스를 최대 6부작으로 만들어줘."""


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
