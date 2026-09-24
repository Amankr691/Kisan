import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:8b"
OLLAMA_TIMEOUT = 120


SUPPORTED_LANGUAGES = {
    "English": "English",
    "Hindi": "Hindi",
    "Bengali": "Bengali",
}


def generate_assistant_response(message, language="English"):
    """
    Generate a response from the local Ollama model.

    The response language is controlled by the language selected
    by the user in the KISAAN AI Assistant.
    """

    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")

    if language not in SUPPORTED_LANGUAGES:
        language = "English"

    response_language = SUPPORTED_LANGUAGES[language]

    prompt = f"""
You are KISAAN AI Assistant, an agricultural assistant for farmers in India.

Your job is to understand the user's actual question and answer it directly.

LANGUAGE RULES:
1. The selected response language is: {response_language}
2. Always reply in {response_language}.
3. If the selected language is Hindi, write naturally in Hindi using Devanagari script.
4. If the selected language is Bengali, write naturally in Bengali script.
5. If the selected language is English, reply in clear simple English.
6. The user's question may itself be written in English, Hindi, Bengali, or mixed language.
7. Understand the meaning of the question before answering.
8. Do not translate the question back to the user unless asked.
9. Use natural, standard agricultural terminology in the selected language.
10. For Bengali, prefer standard terms such as "দোআঁশ মাটি" and "এঁটেল-দোআঁশ মাটি" instead of awkward transliterations of English words.
11. If a technical term may be unclear, write the Bengali or Hindi term first and the English term in parentheses.

RESPONSE RULES:
- Answer the question directly.
- Do NOT introduce yourself unless the user asks who you are.
- Do NOT respond with generic statements such as:
  "How can I help you?"
  "What agricultural topic do you want to know about?"
  when the user has already asked a clear question.
- Do NOT change the subject.
- Use simple language suitable for farmers.
- Keep normal answers concise but useful.
- For agricultural questions, give practical and relevant information.
- If appropriate, mention crops, soil types, seasons, irrigation, diseases,
  fertilizers, weather, machinery, or government schemes.
- Never invent information when uncertain.
- If the question genuinely lacks necessary information, ask one short
  clarification question.

EXAMPLE:

User:
ধান চাষের জন্য কোন ধরনের মাটি ভালো?

Correct Bengali-style answer:
ধান চাষের জন্য উর্বর দোআঁশ বা এঁটেল-দোআঁশ মাটি ভালো। যে মাটি পানি কিছু সময়
ধরে রাখতে পারে এবং জৈব পদার্থসমৃদ্ধ, সেই মাটি ধান চাষের জন্য বেশি উপযোগী।

User message:
{message}

Answer only the user's question in {response_language}:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        "options": {
            "temperature": 0.2                                                                                                                                                                                  
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get("response", "").strip()

        if not answer:
            raise RuntimeError("Ollama returned an empty response.")

        return answer

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama took too long to respond."
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama request failed: {exc}"
        )