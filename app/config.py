from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    test_database_hostname: str
    test_database_port: int
    test_database_name: str
    test_database_username: str
    test_database_password: str

    class Config:
        env_file = '.env'


settings = Settings()
