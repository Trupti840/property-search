from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://app:app@localhost:5433/propsearch"
    opensearch_url: str = "http://localhost:9200"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""

settings = Settings()
