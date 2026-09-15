"""AI-assisted inspection: ask Gemini to compare two stimuli against a
stated intended manipulation, returning a structured verdict.
"""

import base64
import json
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

PROMPT_TEMPLATE = """You are inspecting two visualization stimuli (bar charts) generated for a controlled experiment.

The researcher's INTENDED manipulation is: gridlines only. One image has gridlines OFF, the other has gridlines ON. Every other visual property (underlying data, bar colors, font, axis range, chart dimensions, tick spacing, background) is supposed to be identical.

Carefully compare the two images. Identify any differences OTHER than gridlines - for example: font size, bar color, axis range/scale, chart dimensions, tick spacing, background color, or anything else visually different.

Respond with ONLY valid JSON, no other text, in exactly this format:
{"unexpected_differences": ["short description of each unexpected difference, empty list if none"], "verdict": "VALID" or "CONFOUND_DETECTED"}
"""


def _load_image_part(path):
    with open(path, "rb") as f:
        data = f.read()
    return {"type": "image", "data": base64.b64encode(data).decode("utf-8"), "mime_type": "image/png"}


def inspect_pair_ai(image_path_a, image_path_b, max_retries=5):
    """Send both images + the manipulation prompt to Gemini, return a parsed verdict dict.

    Retries with exponential backoff on rate-limit errors, since the free
    tier's actual quota (observed: 20-request bucket) is stricter than a
    fixed sleep can reliably stay under - a burst of calls can still trip
    it even with throttling between calls.
    """
    delay = 20  # seconds, starting point based on the observed "retry in ~30s" hint
    for attempt in range(max_retries):
        try:
            interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=[
                    {"type": "text", "text": PROMPT_TEMPLATE},
                    _load_image_part(image_path_a),
                    _load_image_part(image_path_b),
                ],
            )
            break
        except Exception as e:
            is_rate_limit = "429" in str(e) or "RateLimit" in type(e).__name__ or "quota" in str(e).lower()
            if is_rate_limit and attempt < max_retries - 1:
                print(f"  rate limited, waiting {delay}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(delay)
                delay *= 1.5
                continue
            raise

    raw_text = interaction.output_text.strip()
    try:
        cleaned = raw_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return {"unexpected_differences": [], "verdict": "PARSE_ERROR", "raw_text": raw_text}

    return parsed