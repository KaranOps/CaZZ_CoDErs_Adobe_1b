import requests
import re
persona ="Travel planner"
job = "Plan a trip of 4 days for a group of 10 college friends."
max_queries = 5
# Format the messages into a single prompt
system_msg = """
You are an intelligent agent having persona **{persona} tasked with **decomposing this job** into **{max_queries} distinct and highly specific sub-queries**, considering the persona’s unique goals, preferences, and constraints.""".format(persona=persona, job=job, max_queries=max_queries)

user_msg = "I want to explore different cusines and location"
prompt = f"{system_msg}\n\nUser: {user_msg}\nAssistant:"



# Make request to the completions endpoint
response = requests.post("http://localhost:8000/v1/completions/qwen", json={
    "prompt": prompt,
    "max_tokens": 512,
    "temperature": 0,
    "stop": ["</s>", "\nUser:"]  # Stop at end of response or next user message
})

try:
    result = response.json()
    if 'choices' in result:
        result = result["choices"][0]["text"].strip()
        print("Raw response:", result , "\n\n")
        queries = []
        for i, query in enumerate(result.split("\n"), 1):
            if re.match(r'^\d+\.', query.strip()):  # Check if line starts with a number
                queries.append(query.strip())
        print("Response:", queries)
    else:
        print("Error: Unexpected response format:", result)
except Exception as e:
    print("Error processing response:", str(e))
    print("Raw response:", response.text)