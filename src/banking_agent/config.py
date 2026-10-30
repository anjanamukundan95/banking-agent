from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_ai_project_endpoint: str
    model_name: str
    azure_search_endpoint: str
    azure_search_index_name: str
    azure_search_semantic_configuration: str
    azure_ai_agent_name: str
    banking_api_base_url: str
    content_safety_endpoint: str
    application_insights_connection_string: str

    # Microsoft Entra ID
    auth_issuer: str
    auth_audience: str
    auth_jwks_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
