import os
import json
from src.llm_handler import LLMWrapper
from src.pipeline import run_pipeline


def is_valid_collection(folder_path):
    return (
        os.path.isdir(folder_path)
        and os.path.basename(folder_path).startswith("Collection_")
        and os.path.isfile(os.path.join(folder_path, "challenge1b_input.json"))
    )


if __name__ == "__main__":
    llm = LLMWrapper()

    # Change to input directory to find collections
    input_dir = "input"
    collections = sorted(
        [
            f
            for f in os.listdir(input_dir)
            if is_valid_collection(os.path.join(input_dir, f))
        ]
    )

    for collection_name in collections:
        collection_dir = os.path.join(input_dir, collection_name)
        input_path = os.path.join(collection_dir, "challenge1b_input.json")
        output_path = os.path.join(collection_dir, "challenge1b_output.json")

        print(f"\n🔍 Processing: {collection_name}")
        with open(input_path) as f:
            input_data = json.load(f)

        result = run_pipeline(input_data, llm, collection_dir=collection_dir)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"✅ Output written to: {output_path}")

    llm.close()
