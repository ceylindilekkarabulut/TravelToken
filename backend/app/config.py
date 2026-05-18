from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://throne:throne@localhost:5432/throne_travel"
    redis_url: str = "redis://localhost:6379/0"

    openai_api_key: str = ""
    amadeus_client_id: str = ""
    amadeus_client_secret: str = ""
    google_maps_api_key: str = ""

    solana_rpc_url: str = "https://api.devnet.solana.com"
    backend_authority_keypair_path: str = "./keypairs/authority.json"

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
