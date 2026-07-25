from agents.resume_agent import run as resume_agent
from agents.career_agent import run as career_agent
from agents.learning_agent import run as learning_agent
from agents.interview_agent import run as interview_agent
from agents.job_agent import run as job_agent


def detect_agent(prompt: str):
    prompt = prompt.lower()

    if any(word in prompt for word in [
        "resume", "ats", "cv", "cover letter"
    ]):
        return "resume"

    elif any(word in prompt for word in [
        "career", "switch", "future", "goal"
    ]):
        return "career"

    elif any(word in prompt for word in [
        "learn", "course", "study", "roadmap"
    ]):
        return "learning"

    elif any(word in prompt for word in [
        "interview", "question", "mock interview"
    ]):
        return "interview"

    elif any(word in prompt for word in [
        "job", "apply", "linkedin", "company"
    ]):
        return "job"

    return "career"


def execute(prompt, history=None):

    agent = detect_agent(prompt)

    if agent == "resume":
        return resume_agent(prompt, history)

    elif agent == "career":
        return career_agent(prompt, history)

    elif agent == "learning":
        return learning_agent(prompt, history)

    elif agent == "interview":
        return interview_agent(prompt, history)

    elif agent == "job":
        return job_agent(prompt, history)

    return career_agent(prompt, history)