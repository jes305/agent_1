import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = "gemini-1.5-flash"

DISCLAIMER = (
    "\n\n⚠️ This is educational information only and not legal advice. "
    "Consult a licensed attorney."
)
