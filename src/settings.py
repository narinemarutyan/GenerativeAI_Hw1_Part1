from pydantic_settings import BaseSettings


class EnvironmentSettings(BaseSettings):
    """
    Keep environmental variables
    """
    GPT_MODEL: str
    KEY: str

    class Config:
        env_file = "src/.env"


ENV_VARS = EnvironmentSettings()
