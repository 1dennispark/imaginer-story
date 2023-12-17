from getpass import getpass
from typing import Optional

import sqlalchemy as sa
import typer
from typing_extensions import Annotated

from . import domain
from .context import Context

app = typer.Typer()


@app.command('init')
def init(
        db_only: Annotated[bool, typer.Option(help='Initialize only database', show_default=False)] = False,
) -> None:
    if not db_only:
        openai_api_key = getpass('openai api key: ')
        with open('.env', 'w') as f:
            f.write(f'OPENAI_API_KEY={openai_api_key}')

    engine = sa.create_engine("sqlite:///./storyai.db")
    with engine.begin() as session:
        domain.Base.metadata.create_all(session)



persona_cmd = typer.Typer()
app.add_typer(persona_cmd, name='persona')


@persona_cmd.command('add')
def add_persona(
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

    with Context() as ctx:
        persona = ctx.persona.add_character(name, age, mbti, gender, description)
        typer.echo(f'Added persona ID: {persona.id}, context: {persona.context}')


@persona_cmd.command('print')
def all_persona() -> None:
    with Context() as ctx:
        personas = ctx.persona.get_all_characters()
        for persona in personas:
            typer.echo(f'Persona ID: {persona.id}, Name: {persona.name} Context: {persona.context}')


synopsis_cmd = typer.Typer()
app.add_typer(synopsis_cmd, name='synopsis')


@synopsis_cmd.command('add')
def add_synopsis(
        theme: Annotated[Optional[str], typer.Option(help='Theme of the synopsis')] = None,
        persona_id: Annotated[Optional[int], typer.Option(help='ID of the persona to use')] = None,
) -> None:
    if theme is None:
        theme = input('Theme: ')
    if persona_id is None:
        persona_id = int(input('Character ID: '))

    with Context() as ctx:
        synopsis = ctx.synopsis.add_synopsis(theme, persona_id)
        typer.echo(f'Added synopsis ID: {synopsis.id}, content: {synopsis.content}')


@synopsis_cmd.command('print')
def all_synopsis() -> None:
    with Context() as ctx:
        synopses = ctx.synopsis.get_all_synopses()
        for synopsis in synopses:
            typer.echo(f'Synopsis ID: {synopsis.id}, Character ID: {synopsis.character_id}, Theme: {synopsis.theme}')


@synopsis_cmd.command('show')
def show_synopsis(
        synopsis_id: Annotated[int, typer.Option(help='ID of the synopsis to show')],
):
    with Context() as ctx:
        synopsis = ctx.synopsis.get_synopsis(synopsis_id)
        typer.echo(f"Synopsis: \n{synopsis.content}")


def main():
    app()