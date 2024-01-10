from getpass import getpass
from typing import Optional

import httpx
import pydantic
import sqlalchemy as sa
import typer
from typing_extensions import Annotated

from . import domain, models
from .settings import Settings

app = typer.Typer()


@app.command('init')
def init() -> None:
    settings = Settings()
    engine = sa.create_engine(settings.mysql_url)
    with engine.begin() as session:
        domain.Base.metadata.create_all(session)


@app.command('serve')
def serve(
        port: Annotated[int, typer.Option(help='Port to serve on', show_default=False)] = 8080,
        log_level: Annotated[str, typer.Option(help='Log level', show_default=False)] = 'debug',
        init_db: Annotated[bool, typer.Option(help='Initialize database', show_default=False)] = True,
) -> None:
    import uvicorn
    from . import server
    from uvicorn.config import LOGGING_CONFIG

    LOGGING_CONFIG['loggers']['storyai'] = {"handlers": ["default"], "level": log_level.upper(), "propagate": False}
    if init_db:
        init()

    uvicorn.run(
        server.app,
        host='0.0.0.0',
        port=port,
        log_config=LOGGING_CONFIG,
    )


persona_cmd = typer.Typer()
app.add_typer(persona_cmd, name='persona')


@persona_cmd.command('add')
def add_persona(
        api_target: Annotated[str, typer.Option(help='Name of the persona')] = "http://localhost:8080",
        name: Annotated[Optional[str], typer.Option(help='Name of the persona')] = None,
        age: Annotated[Optional[int], typer.Option(help='Age of the persona')] = None,
        gender: Annotated[Optional[domain.Gender], typer.Option(help='Gender of the persona')] = None,
        mbti: Annotated[Optional[str], typer.Option(help='MBTI of the persona')] = None,
        description: Annotated[Optional[str], typer.Option(help='Description of the persona')] = None,
) -> None:
    if name is None:
        name = input('Name: ')
    if age is None:
        age = int(input('Age: '))
    if gender is None:
        gender = domain.Gender(input('Gender: '))
    if mbti is None:
        mbti = input('MBTI: ')
    if description is None:
        description = input('Description: ')

    inputs = models.AddCharacterInput(
        name=name,
        age=age,
        gender=gender,
        mbti=mbti,
        description=description,
    )

    resp = httpx.post(api_target + '/personas', json=inputs.model_dump(mode='json')).raise_for_status()
    persona = models.Character.model_validate(resp.json())
    typer.echo(f'Added persona ID: {persona.id}, context: {persona.context}')


@persona_cmd.command('print')
def all_persona(
        api_target: Annotated[str, typer.Option(help='Name of the persona')] = "http://localhost:8080",
) -> None:
    resp = httpx.get(api_target + '/personas').raise_for_status()
    personas = [models.Character.model_validate(r) for r in resp.json()]
    for persona in personas:
        typer.echo(f'Persona ID: {persona.id}, Name: {persona.name} Context: {persona.context}')


synopsis_cmd = typer.Typer()
app.add_typer(synopsis_cmd, name='synopsis')


@synopsis_cmd.command('add')
def add_synopsis(
        api_target: Annotated[str, typer.Option(help='Name of the persona')] = "http://localhost:8080",
        theme: Annotated[Optional[str], typer.Option(help='Theme of the synopsis')] = None,
        persona_id: Annotated[Optional[int], typer.Option(help='ID of the persona to use')] = None,
) -> None:
    if theme is None:
        theme = input('Theme: ')
    if persona_id is None:
        persona_id = int(input('Character ID: '))

    inputs = models.AddSynopsisInput(
        theme=theme,
        character_id=persona_id,
    )
    resp = httpx.post(api_target + f'/synopses', json=inputs.model_dump(mode='json')).raise_for_status()
    synopsis = models.Synopsis.model_validate(resp.json())
    typer.echo(f'Added synopsis ID: {synopsis.id}, content: {synopsis.content}')


@synopsis_cmd.command('print')
def all_synopsis(
        api_target: Annotated[str, typer.Option(help='Name of the persona')] = "http://localhost:8080",
) -> None:
    resp = httpx.get(api_target + '/synopses').raise_for_status()
    synopses = [models.Synopsis.model_validate(r) for r in resp.json()]
    for synopsis in synopses:
        typer.echo(f'Synopsis ID: {synopsis.id}, Character ID: {synopsis.character_id}, Theme: {synopsis.theme}')


@synopsis_cmd.command('show')
def show_synopsis(
        api_target: Annotated[str, typer.Option(help='Name of the persona')] = "http://localhost:8080",
        synopsis_id: Annotated[Optional[int], typer.Option(help='ID of the synopsis to show')] = None,
):
    if synopsis_id is None:
        synopsis_id = int(input('Synopsis ID: '))

    resp = httpx.get(api_target + f'/synopses/{synopsis_id}').raise_for_status()
    synopsis = models.Synopsis.model_validate(resp.json())
    typer.echo(f"Synopsis: \n{synopsis.content}")


def main():
    app()
