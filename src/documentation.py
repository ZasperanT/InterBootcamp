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

def regenerate_meeting_record(
    refined_transcript: str,
    candidate_record: dict,
    verification: dict
) -> dict:
    """
    Regenerate the meeting record using verification feedback.

    The refined transcript remains the only source of truth.
    """

    import json

    instructions = load_documentation_prompt()

    verification_feedback = json.dumps(
        verification,
        indent=2,
        ensure_ascii=False
    )

    candidate_json = json.dumps(
        candidate_record,
        indent=2,
        ensure_ascii=False
    )

    input_text = f"""
REFINED TRANSCRIPT:
{refined_transcript}

CANDIDATE MEETING RECORD:
{candidate_json}

VERIFICATION RESULTS:
{verification_feedback}

Your task is to produce a corrected meeting record.

IMPORTANT:
- The refined transcript is the only source of truth.
- Keep claims that are supported by the transcript.
- Remove or correct claims that are contradicted by the transcript.
- Do not turn uncertain proposals into confirmed decisions.
- Do not invent owners, deadlines, decisions, or tasks.
- If an owner or deadline is not explicitly stated, use "Unspecified".
- Preserve the original meaning of the transcript.
- Return ONLY valid JSON using the required meeting-record structure.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        instructions=instructions,
        input=input_text
    )

    return json.loads(response.output_text)