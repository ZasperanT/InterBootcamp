import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_documentation_prompt() -> str:
    """
    Load the meeting documentation instructions.
    """

    prompt_path = Path("prompts/documentation.txt")

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


def generate_meeting_record(refined_transcript: str) -> dict:
    """
    Generate a structured meeting record from a refined transcript.
    """

    instructions = load_documentation_prompt()

    response = client.responses.create(
        model="gpt-6-luna",
        instructions=instructions,
        input=refined_transcript
    )

    result = response.output_text

    return json.loads(result)