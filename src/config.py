from dataclasses import dataclass
import os


@dataclass
class Settings:
    openai_api_key: str | None
    openai_base_url: str
    openai_model: str
    elevenlabs_api_key: str | None
    elevenlabs_voice_id: str | None
    pexels_api_key: str | None



def load_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY"),
        elevenlabs_voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        pexels_api_key=os.getenv("PEXELS_API_KEY"),
    )
