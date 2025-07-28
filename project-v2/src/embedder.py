import requests
import numpy as np

class MiniLMRemoteEmbedder:
    def __init__(self, endpoint_url="http://127.0.0.1:8000/v1/completions/nomic"):
        self.endpoint_url = endpoint_url
        self.dimension = 768  # Adjust based on your MiniLM variant

    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding from MiniLM via FastAPI."""
        payload = {
            "prompt": text
        }

        try:
            response = requests.post(self.endpoint_url, json=payload)
            response.raise_for_status()
            data = response.json()

            if "embedding" in data:
                embedding = np.array(data["embedding"], dtype=np.float32)
                if embedding.shape[0] != self.dimension:
                    raise ValueError(f"Expected dimension {self.dimension}, got {embedding.shape[0]}")
                return embedding

            raise ValueError(f"Invalid response format: {data}")

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to embedding server: {e}")
        except ValueError as e:
            raise ValueError(f"Failed to parse embedding: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")
        
