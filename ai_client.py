import time
import requests

from config import API_KEY, MODEL, API_URL

class APIError(Exception):
    """Custom exception for API errors."""
    pass

def ask_ai(question: str,retries: int =3) -> dict:

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    for attempt in range(retries):

        try:
            start_time = time.perf_counter()

            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )

            elapsed = time.perf_counter() - start_time

            try:
                data = response.json()
            except ValueError:
                data = {}

            if response.status_code in (408, 429, 502, 503):
                if attempt < retries - 1:
                    retry_after = response.headers.get("Retry-After")

                    try:
                        wait = float(retry_after) if retry_after else 2 ** attempt
                    except ValueError:
                        wait = 2 ** attempt

                    time.sleep(min(wait, 30))
                    continue

            if not response.ok:
                error = data.get("error", {})
                message = error.get(
                    "message",
                    response.text[:300]
                )

                raise APIError(
                    f"HTTP {response.status_code}: {message}"
                )

            if "error" in data:
                raise APIError(data["error"].get("message", "API error"))

            choices = data.get("choices")

            if not isinstance(choices, list) or not choices:
                raise APIError("API returned no answer choices.")

            message = choices[0].get("message", {})
            answer = message.get("content")

            if not isinstance(answer, str) or not answer.strip():
                raise APIError("API returned an empty or invalid answer.")

            return {
                "answer": answer,
                "model": data.get("model"),
                "usage": data.get("usage", {}),
                "response_time": round(elapsed, 2),
                "generation_id": response.headers.get("X-Generation-Id")
            }

        except requests.exceptions.Timeout:
            if attempt == retries - 1:
                raise APIError("Request timed out after multiple attempts.")

        except requests.exceptions.ConnectionError:
            if attempt == retries - 1:
                raise APIError("Unable to connect to OpenRouter.")

        if attempt < retries - 1:
            time.sleep(2 ** attempt)

    raise APIError("Request failed.")