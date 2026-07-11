import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from worldline.config import WorldlineSettings


class Settings(WorldlineSettings, BaseSettings):
    """Sift configuration settings."""

    model_config = SettingsConfigDict(extra="allow", env_file=".env")

    langfuse_public_key: Optional[str] = ""
    langfuse_secret_key: Optional[str] = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    dspy_cachedir: str = "/tmp/dspy_cache"


settings = Settings()
os.environ["DSPY_CACHEDIR"] = settings.dspy_cachedir
