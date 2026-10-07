import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_refinement_prompt() -> str:
    """
    Load the transcript refinement instructions from the prompt file.
    """

    prompt_path = Path("prompts/refinement.txt")

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


def refine_transcript(raw_transcript: str) -> str:
    """
    Refine a raw transcript using the terminology-refinement LLM.
    """

    instructions = load_refinement_prompt()

    response = client.responses.create(
        model="gpt-6-luna",
        instructions=instructions,
        input=raw_transcript
    )

    return response.output_text