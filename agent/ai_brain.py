import json
import time
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

# Maximum time for one Ollama request.
# 900 seconds = 15 minutes.
OLLAMA_TIMEOUT = 900

# Number of times to retry a failed request.
MAX_RETRIES = 2


def _clean_json_text(text):
    """
    Clean common formatting problems from an Ollama JSON response.
    """

    if not isinstance(text, str):
        return text

    text = text.strip()

    # Remove markdown code fences if the model adds them.
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def ask_ollama(
    prompt,
    system="You are a helpful AI assistant.",
    temperature=0.4,
    max_retries=MAX_RETRIES,
):
    """
    Send a prompt to the local Ollama model.

    Returns:
        Python object parsed from Ollama's JSON response.

    Raises:
        RuntimeError if Ollama cannot complete the request.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": temperature,
        },
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    last_error = None

    for attempt in range(max_retries + 1):

        try:
            print(
                f"   Ollama request "
                f"(attempt {attempt + 1}/{max_retries + 1})..."
            )

            with urllib.request.urlopen(
                request,
                timeout=OLLAMA_TIMEOUT,
            ) as response:

                raw = response.read().decode("utf-8")

            outer = json.loads(raw)

            response_text = outer.get("response", "")

            if not response_text:
                raise RuntimeError(
                    "Ollama returned an empty response."
                )

            response_text = _clean_json_text(response_text)

            try:
                result = json.loads(response_text)
            except json.JSONDecodeError as json_error:

                # Sometimes the model may return slightly malformed JSON.
                print("   Warning: Ollama returned invalid JSON.")
                print(f"   JSON error: {json_error}")

                raise RuntimeError(
                    "Ollama returned invalid JSON."
                ) from json_error

            print("   Ollama response received successfully.")

            return result

        except TimeoutError as error:

            last_error = error

            print(
                f"   Ollama timed out after "
                f"{OLLAMA_TIMEOUT} seconds."
            )

            if attempt < max_retries:
                print("   Retrying Ollama request...")
                time.sleep(3)

        except urllib.error.URLError as error:

            last_error = error

            print(
                f"   Could not connect to Ollama: {error}"
            )

            if attempt < max_retries:
                print("   Retrying in 3 seconds...")
                time.sleep(3)

        except ConnectionError as error:

            last_error = error

            print(
                f"   Connection error: {error}"
            )

            if attempt < max_retries:
                print("   Retrying in 3 seconds...")
                time.sleep(3)

        except Exception as error:

            last_error = error

            print(
                f"   Ollama error: "
                f"{type(error).__name__}: {error}"
            )

            if attempt < max_retries:
                print("   Retrying in 3 seconds...")
                time.sleep(3)

    raise RuntimeError(
        "Ollama failed after all retry attempts. "
        f"Last error: {last_error}"
    )