def generate_multiple_queries(persona, job, llm, max_queries=5):
    prompt = f"""
Persona: {persona}
Job to be done: {job}

You are an intelligent agent tasked with **decomposing this job** into **{max_queries} distinct and highly specific sub-queries**, considering the persona’s unique goals, preferences, and constraints.

Each query must:
- Focus on a **single, clearly defined aspect** of the task.
- Be independently useful for retrieving relevant documents (via embeddings).
- Avoid repeating the same type of query with different wording.
- Cover **diverse perspectives**: logistics, planning, risks, resources, preferences, etc.
- Maximize depth and granularity to reach the maximum number of **unique and non-redundant** queries.

Think like an expert planner and information retriever.

📌 Output format:
Return only a numbered list of sub-queries.
Each query should be self-contained and start directly with an action or inquiry.
Do not include explanations, metadata, or extra commentary.

Start generating the sub-queries now.
"""  
    response = llm.generate(prompt)
    return [q for q in response.split("\n") if q.strip()]
