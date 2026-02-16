import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def detect_vulnerability(baseline_text, injected_text, payload):

    prompt = f"""
You are a professional penetration tester.

Compare BASELINE and INJECTED HTTP responses.

Payload used:
{payload}

If vulnerability exists return ONLY one label from:
SQL Injection
XSS
LFI
RCE
SSRF
SSTI
NONE

BASELINE:
{baseline_text[:2000]}

INJECTED:
{injected_text[:2000]}
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception:
        return "NONE"