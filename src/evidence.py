import re


def segment_transcript(
    transcript: str,
    max_chars: int = 1200
) -> list[dict]:
    """
    Split a refined transcript into numbered evidence segments.

    The original transcript text is preserved.
    """

    if not transcript.strip():
        return []

    # Normalize line endings
    transcript = transcript.replace("\r\n", "\n")

    # Split primarily on blank lines
    blocks = re.split(r"\n\s*\n", transcript)

    segments = []

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        # If a block is small enough, keep it as one segment
        if len(block) <= max_chars:

            segments.append({
                "segment_id": f"segment_{len(segments) + 1:03d}",
                "text": block
            })

        else:
            # Split very large blocks into smaller pieces
            words = block.split()

            current = []

            for word in words:

                candidate = " ".join(current + [word])

                if len(candidate) > max_chars and current:

                    segments.append({
                        "segment_id": f"segment_{len(segments) + 1:03d}",
                        "text": " ".join(current)
                    })

                    current = [word]

                else:
                    current.append(word)

            if current:

                segments.append({
                    "segment_id": f"segment_{len(segments) + 1:03d}",
                    "text": " ".join(current)
                })

    return segments