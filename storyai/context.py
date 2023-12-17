import sqlalchemy
from sqlalchemy import orm

from . import services, completion
from .settings import Settings


class Context:
    def __init__(self):
        self._synopsis = None
        self._persona = None
        self._settings = None
        self._db = None
        self._completer = None
        self._services = None
        self._session = None

    def __enter__(self) -> 'Context':
        return self

    def __exit__(self, *args, **kwargs):
        if self._session is not None:
            self._session.close()
            self._session = None

    @property
    def settings(self) -> Settings:
        if self._settings is None:
            self._settings = Settings()
        return self._settings

    @property
    def db(self):
        if self._session is None:
            engine = sqlalchemy.create_engine("sqlite:///" + self.settings.db_path)
            self._session = orm.Session(engine)
        return self._session

    @property
    def completer(self):
        if self._completer is None:
            self._completer = completion.Completer(self.settings.openai_api_key, self.settings.completion_model)
        return self._completer

    @property
    def persona(self) -> services.PersonaService:
        if self._persona is None:
            self._persona = services.PersonaService(self.db, self.completer)
        return self._persona

    @property
    def synopsis(self) -> services.SynopsisService:
        if self._synopsis is None:
            self._synopsis = services.SynopsisService(self.db, self.completer)
        return self._synopsis
