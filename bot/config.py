from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    users_db: int
    services_db: int
    tg_storage_db: int


class TgBotSettings(BaseSettings):
    token: str


class GSheetsSettings(BaseSettings):
    client_secret_path: str
    service_account_path: str
    cosm_table_id: str


class S3Settings(BaseSettings):
    access_key_id: str
    secret_access_key: str
    region_name: str
    bucket_name: str


class Settings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    redis: RedisSettings
    tg_bot: TgBotSettings
    gsheets: GSheetsSettings
    s3: S3Settings


settings = Settings()
