from pathlib import Path
import subprocess


SUPPORTED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".mp4",
    ".mpeg",
    ".mpga",
    ".webm",
}


def validate_audio_file(audio_path: str) -> None:
    """
    Validate that the supplied file exists and contains readable audio.

    Raises
    ------
    ValueError
        If the file is invalid or unsupported.
    """

    path = Path(audio_path)

   
    if not path.exists():
        raise ValueError(f"Audio file not found: {audio_path}")

    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {audio_path}")

   
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format: {path.suffix}. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

  
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "a:0",
                "-show_entries", "stream=codec_name",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    except subprocess.CalledProcessError:
        raise ValueError(
            "The audio file could not be read. "
            "It may be corrupted or invalid."
        )

  
    codec = result.stdout.strip()

    if not codec:
        raise ValueError(
            "The file does not contain a readable audio stream."
        )


    try:
        duration_result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        duration = float(duration_result.stdout.strip())

    except (subprocess.CalledProcessError, ValueError):
        raise ValueError(
            "Could not determine the audio duration."
        )

    if duration <= 0:
        raise ValueError("The audio file is empty.")