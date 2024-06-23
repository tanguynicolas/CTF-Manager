from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    url: str = "mongodb://localhost/"
    db_name: str = "ctf_manager"

    model_config = SettingsConfigDict(env_prefix="mongodb_", extra="allow")

class KafkaSettings(BaseSettings):
    enable: bool = False
    hostname: str = "localhost"
    port: str = "9092"
    topic: str = "ctfmanager"

    model_config = SettingsConfigDict(env_prefix="kafka_", extra="allow")

database_settings = DatabaseSettings()
kafka_settings = KafkaSettings()
