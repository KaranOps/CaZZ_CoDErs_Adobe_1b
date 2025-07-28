def format_messages(messages):
    # If messages is a list of dicts, convert to prompt string
    if isinstance(messages, list):
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"{msg['content']}\n"
            elif msg["role"] == "user":
                prompt += f"User: {msg['content']}\nAssistant:"
            elif msg["role"] == "assistant":
                prompt += f"Assistant: {msg['content']}\n"
        return prompt
    return messages  # If already a string

def refine_sections(sections, persona, job, llm):
    refined = []
    for sec in sections:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that rewrites text chunks to be more relevant and tailored."},
            {"role": "user", "content": f"Rewrite the following chunk to better serve the persona's task. Respond with only the refined text.\n\nPersona: {persona}\nTask: {job}\nChunk: {sec['body']}"}

        ]
        prompt = format_messages(messages)
        llm_output = llm.generate(prompt)
        # ...parse llm_output as needed...
        refined.append({
            "document": sec.get("source", ""),
            "refined_text": llm_output,
            "page_number": sec.get("page", None)
        })
    return refined