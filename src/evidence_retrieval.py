import re
from collections import Counter


STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "is",
    "are",
    "was",
    "were",
    "be",
    "before",
    "after",
    "will",
    "would",
    "should",
    "this",
    "that",
    "it",
    "as",
    "by",
    "from",
    "at",
    "you",
    "your",
    "their",
    "they",
    "he",
    "she",
    "we",
    "our",
}


def tokenize(text: str) -> list[str]:
    """
    Convert text into normalized word tokens.
    """

    words = re.findall(
        r"\b[a-zA-Z0-9€£$]+\b",
        text.lower()
    )

    return [
        word
        for word in words
        if word not in STOPWORDS
    ]


def score_segment(
    claim_text: str,
    segment_text: str
) -> float:
    """
    Calculate a simple lexical relevance score.

    Score is based on overlap between meaningful
    words in the claim and the segment.
    """

    claim_tokens = tokenize(claim_text)
    segment_tokens = tokenize(segment_text)

    if not claim_tokens or not segment_tokens:
        return 0.0

    claim_counts = Counter(claim_tokens)
    segment_counts = Counter(segment_tokens)

    overlap = 0

    for word in claim_counts:

        if word in segment_counts:
            overlap += min(
                claim_counts[word],
                segment_counts[word]
            )

    return overlap / len(claim_counts)


def retrieve_evidence(
    claim: dict,
    segments: list[dict],
    top_k: int = 3
) -> list[dict]:
    """
    Retrieve the most relevant transcript segments
    for a structured claim.
    """

    # Combine all meaningful claim fields
    claim_parts = []

    if claim.get("task"):
        claim_parts.append(claim["task"])

    if claim.get("owner"):
        claim_parts.append(claim["owner"])

    if claim.get("deadline"):
        claim_parts.append(claim["deadline"])

    if claim.get("decision"):
        claim_parts.append(claim["decision"])

    claim_text = " ".join(claim_parts)

    scored_segments = []

    for segment in segments:

        score = score_segment(
            claim_text,
            segment["text"]
        )

        scored_segments.append({
            "segment_id": segment["segment_id"],
            "text": segment["text"],
            "score": score
        })

    # Highest score first
    scored_segments.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # Return only useful evidence
    return [
        segment
        for segment in scored_segments[:top_k]
        if segment["score"] > 0
    ]