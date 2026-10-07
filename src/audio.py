import subprocess
import tempfile
from pathlib import Path


def get_audio_duration(audio_path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


def split_audio(
    audio_path: str,
    output_dir: str | None = None,
    chunk_duration: int = 300
):
    audio_path = Path(audio_path)

    
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="meeting_chunks_")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = output_dir / "chunk_%03d.wav"

    command = [
        "ffmpeg",
        "-i", str(audio_path),
        "-f", "segment",
        "-segment_time", str(chunk_duration),
        "-c", "copy",
        str(output_pattern)
    ]

    subprocess.run(command, check=True)

    chunks = sorted(output_dir.glob("chunk_*.wav"))

    return [str(chunk) for chunk in chunks]