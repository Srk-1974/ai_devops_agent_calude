from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ado_organization: str
    ado_project: str
    ado_pat: str
    azure_openai_endpoint: str
    azure_openai_api_key: str
    environment: str = "development"
    cosmos_endpoint: Optional[str] = None
    cosmos_key: Optional[str] = None
    cosmos_database: str = "DevOpsAgent"
    cosmos_container: str = "PRAnalysis"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }
