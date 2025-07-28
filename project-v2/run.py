import os
import json
from src.llm_handler import LLMWrapper
from src.pipeline import run_pipeline

def is_valid_collection(folder):
    return os.path.isdir(folder) and folder.startswith("Collection_") and \
           os.path.isfile(os.path.join(folder, "challenge1b_input.json"))

if __name__ == "__main__":
    llm = LLMWrapper()

    collections = sorted([f for f in os.listdir(".") if is_valid_collection(f)])

    for collection_dir in collections:
        input_path = os.path.join(collection_dir, "challenge1b_input.json")
        output_path = os.path.join(collection_dir, "challenge1b_output.json")

        print(f"\n🔍 Processing: {collection_dir}")
        with open(input_path) as f:
            input_data = json.load(f)

        result = run_pipeline(input_data, llm, collection_dir=collection_dir)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"✅ Output written to: {output_path}")

    llm.close()
