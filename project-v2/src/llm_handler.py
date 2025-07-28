import requests

class LLMWrapper:
    def __init__(self, api_url="http://127.0.0.1:8000/v1/completions/qwen"):
        self.api_url = api_url

    def generate(self, prompt, max_tokens=512, temperature=0, stop=None):
        if stop is None:
            stop = ["</s>", "\nUser:"]
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": stop
        }
        response = requests.post(self.api_url, json=payload)
        result = response.json()
        if 'choices' in result and result['choices']:
            return result['choices'][0]['text'].strip()
        else:
            raise RuntimeError(f"LLM server error: {result}")

    def close(self):
        pass  # No resources to release