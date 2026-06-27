from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from worldline import LoggingSettings


class Settings(LoggingSettings, BaseSettings):
    """Sift configuration settings."""

    model_config = SettingsConfigDict(extra="allow", env_file=".env")

    langfuse_public_key: Optional[str] = ""
    langfuse_secret_key: Optional[str] = ""
    langfuse_host: str = "https://cloud.langfuse.com"


settings = Settings()
