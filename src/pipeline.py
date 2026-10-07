import json
from pathlib import Path
from src.validators import validate_audio_file
from src.transcription import transcribe_full_audio
from src.refinement import refine_transcript
from src.documentation import generate_meeting_record


def process_meeting(audio_path: str, output_dir: str = "outputs") -> dict:
    """
    Run the complete meeting-processing pipeline.

    Pipeline:
        Audio
        -> Validation
        -> Transcription
        -> Refinement
        -> Documentation

    Returns
    -------
    dict
        Structured meeting record.
    """
    try:
     validate_audio_file(audio_path)

     output_dir = Path(output_dir)
     output_dir.mkdir(parents=True, exist_ok=True)

    

     print("\n=== STAGE 1: TRANSCRIPTION ===")

     raw_transcript = transcribe_full_audio(audio_path)
     
     if not raw_transcript.strip():
       raise ValueError("Transcription produced no usable text.")

     raw_transcript_path = output_dir / "raw_transcript.txt"

     with open(raw_transcript_path, "w", encoding="utf-8") as file:
         file.write(raw_transcript)

     print(f"Raw transcript saved to: {raw_transcript_path}")


     print("\n=== STAGE 2: REFINEMENT ===")

     refined_transcript = refine_transcript(raw_transcript)

     refined_transcript_path = output_dir / "refined_transcript.txt"

     with open(refined_transcript_path, "w", encoding="utf-8") as file:
         file.write(refined_transcript)

     print(f"Refined transcript saved to: {refined_transcript_path}")


     print("\n=== STAGE 3: DOCUMENTATION ===")

     meeting_record = generate_meeting_record(refined_transcript)

     meeting_record_path = output_dir / "meeting_record.json"

     with open(meeting_record_path, "w", encoding="utf-8") as file:
         json.dump(
         meeting_record,
         file,
         indent=4,
         ensure_ascii=False
          )

     print(f"Meeting record saved to: {meeting_record_path}")

     return {
        "raw_transcript": raw_transcript,
        "refined_transcript": refined_transcript,
        "meeting_record": meeting_record
     }
    except Exception as error:
       raise RuntimeError(f"Meeting Processing Failed: {error}") from error