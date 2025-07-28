import json
from src.llm_handler import LLMWrapper
from src.pipeline import run_pipeline

if __name__ == "__main__":
    with open("input.json") as f:
        input_data = json.load(f)
    
    print("lora")
    llm = LLMWrapper()
    print("lora")
    result = run_pipeline(input_data, llm)
    print("lora")

    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)

    llm.close()