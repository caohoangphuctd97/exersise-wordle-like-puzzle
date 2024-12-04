from pydantic_settings import BaseSettings
from pydantic.networks import PostgresDsn

class AsyncPostgresDsn(PostgresDsn):
    default_scheme = "postgresql+asyncpg"
    allowed_schemes = {"postgresql+asyncpg", "postgres+asyncpg"}


class DatabaseServiceConfig(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str = "127.0.0.1"

    DATABASE_POOL_SIZE: int = 2
    DATABASE_POOL_MAX: int = 10
    DATABASE_POOL_TIMEOUT: int = 10

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict:
        engine_option = {
            "pool_timeout": self.DATABASE_POOL_TIMEOUT,
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_POOL_MAX,
        }

        return engine_option

    @property
    def ASYNC_DATABASE_URI(self) -> AsyncPostgresDsn:
        url = AsyncPostgresDsn.build(
            scheme=AsyncPostgresDsn.default_scheme,
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
            path=f"{self.DATABASE_NAME}"
        )
        return url.unicode_string()

