import requests

API_KEY = "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"
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def call_ai(prompt):
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Selalu balas dalam bahasa Indonesia dengan gaya yang jelas dan informatif."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(BASE_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

