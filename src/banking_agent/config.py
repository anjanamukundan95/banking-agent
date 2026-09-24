from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_ai_project_endpoint: str
    model_name: str
    azure_search_endpoint: str
    azure_search_index_name: str
    azure_search_semantic_configuration: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
