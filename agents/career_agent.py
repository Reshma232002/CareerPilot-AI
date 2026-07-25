from gemini_engine import generate_ai_content


def run(prompt, history=None):

    system = """
You are CareerPilot AI.

You are an experienced career coach.

Remember previous conversation.

Give personalized career advice.

Be practical and concise.
"""

    conversation = ""

    if history:
        for msg in history:
            conversation += f"{msg['role']}: {msg['content']}\n"

    final_prompt = f"""
{system}

Conversation History:
{conversation}

Current User Question:
{prompt}
"""

    return generate_ai_content(final_prompt)