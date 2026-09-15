"""Bare connectivity check - no images yet, just confirm the key and SDK work."""

from dotenv import load_dotenv
from google import genai

load_dotenv()  # reads .env in the current/parent directories into the environment

client = genai.Client()  # picks up GEMINI_API_KEY from the environment
interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Reply with exactly one word: OK",
)
print(interaction.output_text)