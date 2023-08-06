from typing import Any

from dotenv import find_dotenv
from pydantic import (
    BaseSettings,
    Field,
)

from jwt_validate.constants import Environment


class Config(BaseSettings):
    env_file = find_dotenv('.secrets/.env')
    env_file_encoding = 'utf-8'
    ENVIRONMENT: Environment = Environment.LOCAL
    IDPA_JWKS_CACHE_TIME_SECONDS: int = Field(60 * 60 * 8)
    IDPA_URL: str
    VAL_REQUEST_URL_TOKEN: str


settings = Config(_env_file='.env')

app_configs: dict[str, Any] = {'title': 'JWT-Validation - API'}
