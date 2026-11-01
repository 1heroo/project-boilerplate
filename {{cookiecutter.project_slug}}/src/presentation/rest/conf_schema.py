from pydantic import BaseModel


class FastAPIConfig(BaseModel):
    title: str = '{{ cookiecutter.project_name }}'
    debug: bool = False
    docs_enabled: bool = True
    cors_origins: list[str] = ['*']


class GunicornConfig(BaseModel):
    workers: int = 4
    timeout: int = 120
