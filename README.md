# 🎙️ AI Meeting Assistant

An AI-powered meeting assistant that converts recorded English meetings into accurate transcripts, refined transcripts, and structured meeting documentation.

## Overview

The system processes a recorded meeting through three main stages:

1. Speech-to-text transcription
2. Transcript refinement using an LLM
3. Structured meeting documentation using a separate LLM

The application provides a Streamlit interface where users can upload a meeting recording, process it, inspect the raw and refined transcripts, review the generated meeting record, and download the results.

## System Architecture

```text
Meeting Audio
     │
     ▼
Audio Validation
     │
     ▼
Audio Chunking
     │
     ▼
Speech-to-Text
     │
     ▼
Raw Transcript
     │
     ▼
LLM #1 — Transcript Refinement
     │
     ▼
Refined Transcript
     │
     ▼
LLM #2 — Meeting Documentation
     │
     ▼
Structured Meeting Record
     │
     ├── Meeting Summary
     ├── Topics Discussed
     ├── Key Decisions
     └── Action Items
     
### FFmpeg

FFmpeg is required for audio duration checking and audio chunking.

