import shutil
import subprocess

from config import AUDIO_DIR


def generate_voice(text, output_name="voice.wav"):
    """
    Optional Piper TTS helper.

    The main V1 video pipeline does not require Piper; it creates an
    HD visual-card MP4. If Piper is installed and configured separately,
    this helper can generate narration audio.
    """
    piper = shutil.which("piper")
    if not piper:
        raise RuntimeError(
            "Piper TTS was not found on PATH. "
            "The main video renderer does not require Piper."
        )

    output = AUDIO_DIR / output_name
    result = subprocess.run(
        [piper, "--output_file", str(output)],
        input=text,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr or "Piper failed.")

    return output
