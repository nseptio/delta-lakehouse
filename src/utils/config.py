from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class Config(BaseSettings):
    minio_endpoint_url: str
    minio_access_key: str
    minio_secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class FakerConfig(BaseSettings):
    faculty: int = 15
    program: int = 65
    lecturer: int = 1000
    student: int = 45_000
    room: int = 350
    course: int = 2500
    semester: int = 8
    class_schedule: int = 5000
    registration: int = 200_000

    model_config = SettingsConfigDict(yaml_file="./configs/faker.yaml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)
