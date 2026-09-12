import base64
import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5vl:3b"


def diagnose_leaf(image_path, crop_name=None):
    """
    Analyze a crop leaf image using the local Ollama Qwen2.5-VL model.
    """

    # Read image and convert it to base64
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    crop_text = crop_name if crop_name else "Unknown"

    prompt = f"""
You are an agricultural crop disease diagnostic assistant.

Analyze the plant leaf image carefully.

The farmer says the crop is:
{crop_text}

Identify whether the leaf is healthy or diseased.

If diseased, identify the most likely disease.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "disease_name": "Disease name or Healthy",
    "crop_name": "Crop name",
    "confidence": 85,
    "severity": "Low",
    "symptoms": [
        "Symptom 1",
        "Symptom 2",
        "Symptom 3"
    ],
    "organic_treatment": "Organic treatment recommendation",
    "chemical_treatment": "Chemical treatment recommendation"
}}

Rules:

1. confidence must be a number from 0 to 100.
2. severity must be one of:
   Low
   Medium
   High
   Critical

3. Do not include markdown.
4. Do not include ```json.
5. Do not include explanations outside the JSON.
6. If the image is unclear, reduce the confidence score.
7. Do not invent a disease if the plant appears healthy.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False,
        "format": "json",
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    response_data = response.json()

    raw_result = response_data.get("response")

    if not raw_result:
        raise ValueError(
            "Ollama returned an empty response."
        )

    try:
        diagnosis = json.loads(raw_result)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Ollama returned invalid JSON: {raw_result}"
        ) from error

    if not isinstance(diagnosis, dict):
        raise ValueError(
            "Ollama response was not a JSON object."
        )

    return diagnosis