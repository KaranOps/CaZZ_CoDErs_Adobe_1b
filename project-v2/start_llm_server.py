from llama_cpp import Llama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0
    stop: Optional[List[str]] = ["</s>"]

def start_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    n_threads: int = 4,
    n_ctx: int = 2048
):
    print(f" Starting Server at http://{host}:{port}")
    
    # Load Qwen model
    print(" Loading Qwen model...")
    qwen_llm = Llama(
        model_path="./models/qwen2.5/qwen2.5-0.5b-instruct-q4_k_m.gguf",
        n_threads=n_threads,
        n_ctx=n_ctx
    )

    # Load Nomic embedding model
    # print( Loading Nomic embedding model...")
    nomic_embedder = Llama(
        model_path="./models/nomic-ai/nomic-embed-text-v1.5.f16.gguf",
        embedding=True,
        n_threads=n_threads,
        n_batch=8
    )

    # # Optional: Load MiniLM for comparison (not used in routes here)
    # print(" Loading local MiniLM embedding model...")
    # local_model_path = "./models/minilm"
    # minilm_embedder = SentenceTransformer(local_model_path)
    
    app = FastAPI(title="LLM and Embedding API")
    
    @app.post("/v1/completions/nomic")
    async def create_nomic_embedding(request: CompletionRequest):
        try:
            result = nomic_embedder.create_embedding(request.prompt)
            embedding = result['data'][0]['embedding']
            return {"embedding": embedding}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/v1/completions/qwen")
    async def create_qwen_completion(request: CompletionRequest):
        try:
            response = qwen_llm.create_completion(
                prompt=request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stop=request.stop
            )
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
