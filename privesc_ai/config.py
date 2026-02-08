# privesc-ai/config.py
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Config(BaseModel):
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.2
    max_tokens: int 4000

    class Config:
        frozen = True

config = Config()
