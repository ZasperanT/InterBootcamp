# Meeting Assistant

An AI-powered meeting assistant that converts an English meeting recording into a refined transcript and a structured, evidence-grounded meeting record.

## Overview

The application processes a recorded meeting through the following pipeline:

Audio
→ Audio Validation
→ Chunked Speech-to-Text
→ Raw Transcript
→ Transcript Refinement
→ Meeting Documentation
→ Claim Extraction
→ Evidence Retrieval
→ Person/Role Resolution
→ Consistency Verification
→ Regeneration if Required
→ Final Meeting Record

The application provides a Streamlit interface for uploading a meeting recording, processing it, inspecting the generated outputs, and downloading the results.

---

## Key Features

- Upload English meeting recordings.
- Validate audio files before processing.
- Process long recordings using audio chunking.
- Generate and retain the raw transcript.
- Refine speech-to-text errors while preserving meaning.
- Generate structured meeting documentation.
- Extract decisions and action items as claims.
- Retrieve transcript evidence supporting generated claims.
- Resolve people through explicitly stated roles.
- Verify generated claims against the transcript.
- Classify claims as:
  - Supported
  - Contradicted
  - Uncertain
- Regenerate the meeting record when unsupported or contradicted claims are detected.
- Limit regeneration attempts to prevent infinite loops.
- Display supporting transcript evidence in the UI.
- Download raw transcript, refined transcript, and meeting record.

---

## Architecture

### Stage 1 — Speech-to-Text

The uploaded recording is validated and split into manageable audio chunks.

Each chunk is transcribed independently using the OpenAI speech-to-text API.

The chunk transcripts are combined to produce the raw transcript.

### Stage 2 — Transcript Refinement

The raw transcript is passed to the first LLM stage.

The refinement stage:

- Corrects obvious speech-to-text errors.
- Corrects terminology when the intended term is clear.
- Corrects spelling, grammar, and punctuation.
- Preserves names, numbers, dates, technical terminology, and other entities.
- Preserves negations and uncertainty.
- Does not summarize or invent information.

The refined transcript is retained separately from the raw transcript.

### Stage 3 — Meeting Documentation

The refined transcript is passed to the second LLM stage.

This stage generates a structured meeting record containing:

- Meeting summary
- Topics discussed
- Key decisions
- Action items
  - Task
  - Owner
  - Deadline

The documentation stage is instructed to distinguish proposals from confirmed decisions and to avoid inventing owners or deadlines.

### Stage 4 — Evidence Verification

The generated meeting record is converted into individual claims.

The refined transcript is divided into evidence segments.

For each claim, relevant transcript segments are retrieved using lexical evidence matching.

Person-to-role relationships are also extracted from explicit introductions in the transcript.

The retrieved evidence is then checked by the consistency layer.

Claims are classified as:

- `supported`
- `contradicted`
- `uncertain`

### Stage 5 — Regeneration

If unsupported or contradicted claims are found, the documentation LLM receives:

- The refined transcript
- The candidate meeting record
- The verification results

It then generates a corrected meeting record.

The corrected record is verified again.

Regeneration is bounded to a maximum number of attempts.

The refined transcript remains the source of truth throughout this process.

---

