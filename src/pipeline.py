import json
from pathlib import Path

from src.validators import validate_audio_file
from src.transcription import transcribe_full_audio
from src.refinement import refine_transcript
from src.documentation import (generate_meeting_record,regenerate_meeting_record)

from src.evidence import segment_transcript
from src.claim_extraction import extract_claims
from src.evidence_retrieval import retrieve_evidence
from src.consistency import validate_claim
from src.entities import extract_person_roles


def verify_meeting_record(
    refined_transcript: str,
    meeting_record: dict
) -> dict:
    """
    Verify claims in the generated meeting record against
    evidence from the refined transcript.
    """

    # Split transcript into evidence segments
    segments = segment_transcript(refined_transcript)

    # Extract person -> role relationships
    person_roles = extract_person_roles(refined_transcript)

    # Convert candidate meeting record into claims
    claims = extract_claims(meeting_record)

    verification_results = []

    for claim in claims:

        # Retrieve relevant transcript evidence
        evidence = retrieve_evidence(
            claim,
            segments,
            top_k=3
        )

        # Validate claim against evidence
        result = validate_claim(
            claim,
            evidence,
            person_roles
        )

        verification_results.append(result)

    return {
        "person_roles": person_roles,
        "claims": verification_results
    }


def process_meeting(
    audio_path: str,
    output_dir: str = "outputs"
) -> dict:
    """
    Run the complete meeting-processing pipeline.

    Pipeline:

        Audio
        -> Validation
        -> Transcription
        -> Refinement
        -> Documentation
        -> Evidence Verification
        -> Regeneration if necessary
        -> Final Verification
    """

    try:

        # --------------------------------------------------
        # 1. Validate audio
        # --------------------------------------------------

        validate_audio_file(audio_path)

        output_dir = Path(output_dir)
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------------
        # 2. Transcription
        # --------------------------------------------------

        print("\n=== STAGE 1: TRANSCRIPTION ===")

        raw_transcript = transcribe_full_audio(audio_path)

        if not raw_transcript.strip():
            raise ValueError(
                "Transcription produced no usable text."
            )

        raw_transcript_path = (
            output_dir / "raw_transcript.txt"
        )

        with open(
            raw_transcript_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(raw_transcript)

        print(
            f"Raw transcript saved to: "
            f"{raw_transcript_path}"
        )

        # --------------------------------------------------
        # 3. Transcript refinement
        # --------------------------------------------------

        print("\n=== STAGE 2: REFINEMENT ===")

        refined_transcript = refine_transcript(
            raw_transcript
        )

        refined_transcript_path = (
            output_dir / "refined_transcript.txt"
        )

        with open(
            refined_transcript_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(refined_transcript)

        print(
            f"Refined transcript saved to: "
            f"{refined_transcript_path}"
        )

        # --------------------------------------------------
        # 4. Initial meeting documentation
        # --------------------------------------------------

        print("\n=== STAGE 3: DOCUMENTATION ===")

        meeting_record = generate_meeting_record(
            refined_transcript
        )

        # --------------------------------------------------
        # 5. Verification + regeneration
        # --------------------------------------------------

        max_attempts = 2
        verification = None

        for attempt in range(1, max_attempts + 1):

            print(
                f"\n=== STAGE 4: EVIDENCE VERIFICATION "
                f"(attempt {attempt}/{max_attempts}) ==="
            )

            verification = verify_meeting_record(
                refined_transcript,
                meeting_record
            )

            statuses = [
                result["status"]
                for result in verification["claims"]
            ]

            has_problem = any(
                status in {"uncertain", "contradicted"}
                for status in statuses
            )

            if not has_problem:
                print(
                    "All claims are supported."
                )
                break

            if attempt == max_attempts:
                print(
                    "Maximum verification attempts reached."
                )
                break

            print(
                "Unsupported or contradicted claims found."
            )
            print(
                "Regenerating meeting record..."
            )

            meeting_record = regenerate_meeting_record(
                refined_transcript,
                meeting_record,
                verification
            )

        # --------------------------------------------------
        # 6. Save final meeting record
        # --------------------------------------------------

        meeting_record_path = (
            output_dir / "meeting_record.json"
        )

        with open(
            meeting_record_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                meeting_record,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"\nFinal meeting record saved to: "
            f"{meeting_record_path}"
        )

        # --------------------------------------------------
        # 7. Save final verification
        # --------------------------------------------------

        verification_path = (
            output_dir / "verification.json"
        )

        with open(
            verification_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                verification,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Final verification saved to: "
            f"{verification_path}"
        )

        # --------------------------------------------------
        # 8. Print final verification summary
        # --------------------------------------------------

        print("\n=== FINAL VERIFICATION ===")

        for result in verification["claims"]:

            print(
                f"{result['claim_id']}: "
                f"{result['status']}"
            )

        print(
            "\nMeeting processing complete."
        )

        # --------------------------------------------------
        # 9. Return results to Streamlit
        # --------------------------------------------------

        return {
            "raw_transcript": raw_transcript,
            "refined_transcript": refined_transcript,
            "meeting_record": meeting_record,
            "verification": verification
        }

    except Exception as error:

        raise RuntimeError(
            f"Meeting processing failed: {error}"
        ) from error