import re


ROLE_PATTERNS = [
    r"\bI'?m\s+(?P<name>[A-Z][a-z]+),?\s+and\s+I'?m\s+(?:supposed to be\s+)?(?:an?\s+)?(?P<role>[^.,]+)",
    r"\bI\s+am\s+(?P<name>[A-Z][a-z]+),?\s+and\s+I\s+am\s+(?:an?\s+)?(?P<role>[^.,]+)",
]


def extract_person_roles(transcript: str) -> list[dict]:
    """
    Extract person -> role relationships from explicit introductions.

    Only relationships explicitly stated in the transcript are extracted.
    """

    if not transcript.strip():
        return []

    relationships = []

    for pattern in ROLE_PATTERNS:
        matches = re.finditer(
            pattern,
            transcript,
            flags=re.IGNORECASE
        )

        for match in matches:
            name = match.group("name").strip()
            role = match.group("role").strip()

            relationship = {
                "person": name,
                "role": role
            }

            if relationship not in relationships:
                relationships.append(relationship)

    return relationships