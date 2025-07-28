import json
import re
from src.llm_handler import LLMWrapper

def generate_multiple_queries(persona, job, llm, max_queries=5):
    """
    Generates multiple search queries by asking the LLM for a JSON array.
    This method is highly robust against conversational text and formatting errors.
    """
    # This new prompt explicitly asks for a JSON array. This is the key change.
    prompt = f"""You are an expert at creating concise search queries.
Your task is to generate exactly {max_queries} distinct queries based on a persona and a job to be done.

**Persona:** {persona}
**Job to be done:** {job}

**Instructions:**
Your entire response must be ONLY a single, valid JSON array of strings.
Do not include markdown like ```json or any text before or after the array.

Example format: ["query 1", "query 2", "query 3"]
"""

    response = llm.generate(prompt)
    
    # --- Robust Parsing Logic ---
    # This logic is designed to find and parse the JSON array, 
    # even if the model mistakenly adds text around it.
    try:
        # Use regex to find the JSON array within the response string
        # It looks for content starting with '[' and ending with ']'
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            json_string = match.group(0)
            queries = json.loads(json_string)
            return queries
        else:
            # Fallback for simple cases where the model *might* have just returned JSON
            return json.loads(response)
            
    except (json.JSONDecodeError, TypeError) as e:
        print(f"--- FAILED TO PARSE LLM RESPONSE ---")
        print(f"Error: {e}")
        print(f"Raw Response:\n{response}")
        # If parsing fails, return an empty list so the program doesn't crash.
        return []

if __name__ == "__main__":
    input_data = {
        "persona": {
            "role": "A busy college student on a tight budget"
        },
        "job_to_be_done": {
            "task": "Plan a fun and affordable 4-day trip for a group of 10 friends."
        }
    }
    
    llm = LLMWrapper()

    result = generate_multiple_queries(
        input_data["persona"]["role"], 
        input_data["job_to_be_done"]["task"], 
        llm,
        max_queries=5
    )
    
    print("\n--- Generated Queries ---")
    if result:
        for i, query in enumerate(result, 1):
            print(f"{i}. {query}")
    else:
        print("Could not generate or parse queries.")

    llm.close()