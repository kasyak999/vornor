from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки подключения к базе данных."""

    app_title: str = 'vornor'
    description: str = 'Систеама для торговли криптовалютой'

    postgres_user: str = 'user'
    postgres_password: str = 'mysecretpassword'
    postgres_db: str = 'django'
    postgres_port: str = '5433'
    secret: str = 'SECRET'
    redis_pass: str = 'mystrongpassword'

    DEBUG: bool = False

    @property
    def database_url(self) -> str:
        """Формирует URL подключения к базе."""
        db_host = f'localhost:{self.postgres_port}' if self.DEBUG else 'db'
        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}@{db_host}'
            f'/{self.postgres_db}'
        )

    class Config:
        env_file = '.env'


settings = Settings()
