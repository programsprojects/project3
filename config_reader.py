from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pydantic import Field
from typing import Union, List


# Settings class
class Settings(BaseSettings):
    # Defines a property 'bot_token' of type SecretStr for storing sensitive bot token information.
    bot_token: SecretStr
    # Defines a property 'model_config' of type SettingsConfigDict with default parameters.
    model_config: SettingsConfigDict = SettingsConfigDict(
        # Specifies the default file name (".env") for environment variables.
        env_file=".env",
        # Specifies the default encoding ("utf-8") for the environment file.
        env_file_encoding="utf-8"
    )
    # Defines a secret integer value or a list of secret integers
    is_admin: Union[int, List[int]] = Field(
        None,
        env="ADMIN_ID"
    )


# Initializes an instance of the Settings class and assigns it to the variable 'config'.
config = Settings()
