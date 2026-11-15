import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

if not MODEL:
    raise ValueError("OPENROUTER_MODEL is not set in the environment variables.")