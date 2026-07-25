from gemini_engine import generate_ai_content


def run(prompt, history=None):

    system = """
You are an AI Learning Coach.

Recommend learning roadmaps,
courses,
certifications,
projects,
and study plans.
"""

    conversation = ""

    if history:
        for msg in history:
            conversation += f"{msg['role']}: {msg['content']}\n"

    final_prompt = f"""
{system}

Conversation History:
{conversation}

User Question:
{prompt}
"""

    return generate_ai_content(final_prompt)