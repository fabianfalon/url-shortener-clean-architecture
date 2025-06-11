from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    app_title: str = "URL Shortener"
    app_name: str = "fastapi"
    service_name: str = "url-shortener"
    swagger_url: str = "/docs"


class ServerSettings(BaseSettings):
    """
    Gunicorn server settings
    """

    host: str = "127.0.0.1"
    port: int = 5000
    workers_per_core: int = 1
    max_workers: int | None = None
    graceful_timeout: int = 120
    timeout: int = 120
    keep_alive: int = 5
    base_short_url: str = "http://localhost:5000/"


class LocationSettings(BaseSettings):
    timezone: str = "Europe/Madrid"


class Settings(CommonSettings, ServerSettings, LocationSettings):
    mongo_url: str = None
    memcached_url: str = None
    log_level: str = "info"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

settings = Settings()
