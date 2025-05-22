from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class BotSettings(BaseModel):
    token: str

class DBSettings(BaseModel):
    host: str
    port: int
    database: str
    user: str
    password: str

    @property
    def base_url(self) -> str:
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def url(self) -> str:
        return f"mysql+aiomysql://{self.base_url}"

    @property
    def alembic_url(self) -> str:
        return f"mysql+mysqlconnector://{self.base_url}"

class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"

class Settings(BaseSettings):
    bot: BotSettings
    mysql: DBSettings
    redis: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(env_file=("example.env", ".env"), env_nested_delimiter='_')

settings = Settings()