def build_prompt(context, query):

    prompt = f"""
You are a helpful AI assistant.

Answer the question ONLY using the provided context.

If answer is not present, say:
"I could not find the answer in the context."

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt