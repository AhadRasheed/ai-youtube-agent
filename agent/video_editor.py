import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import FINAL_DIR, IMAGES_DIR


WIDTH = 1920
HEIGHT = 1080
FPS = 30


def _font(size, bold=False):
    candidates = []
    if bold:
        candidates += [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
        ]
    candidates += [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)

    return ImageFont.load_default()


def _wrap(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def _create_scene_image(scene_number, title, narration, output):
    image = Image.new("RGB", (WIDTH, HEIGHT), (13, 17, 27))
    draw = ImageDraw.Draw(image)

    # Simple professional sample-card layout.
    draw.rectangle(
        (60, 60, WIDTH - 60, HEIGHT - 60),
        outline=(75, 160, 230),
        width=5,
    )

    label_font = _font(34, bold=True)
    title_font = _font(68, bold=True)
    body_font = _font(38)

    draw.text(
        (120, 115),
        f"AI YOUTUBE AGENT  •  SCENE {scene_number}",
        font=label_font,
        fill=(120, 190, 255),
    )

    title_lines = _wrap(title, title_font, WIDTH - 240, draw)
    y = 205
    for line in title_lines[:2]:
        draw.text((120, y), line, font=title_font, fill=(245, 248, 255))
        y += 82

    # Show a readable excerpt from the narration.
    excerpt = narration.strip()
    if len(excerpt) > 520:
        excerpt = excerpt[:517].rsplit(" ", 1)[0] + "..."

    body_lines = _wrap(excerpt, body_font, WIDTH - 300, draw)
    y += 40
    for line in body_lines[:9]:
        draw.text((150, y), line, font=body_font, fill=(215, 222, 235))
        y += 52

    draw.text(
        (120, HEIGHT - 125),
        "Educational sample • Generated locally with Ollama",
        font=_font(28),
        fill=(150, 160, 175),
    )

    image.save(output, "JPEG", quality=94)


def _write_concat_file(scene_paths, durations, concat_path):
    with open(concat_path, "w", encoding="utf-8", newline="\n") as f:
        for path, duration in zip(scene_paths, durations):
            safe = str(path).replace("\\", "/").replace("'", r"'\''")
            f.write(f"file '{safe}'\n")
            f.write(f"duration {duration:.2f}\n")

        # FFmpeg concat demuxer requires the last file to be repeated.
        if scene_paths:
            safe = str(scene_paths[-1]).replace("\\", "/").replace("'", r"'\''")
            f.write(f"file '{safe}'\n")


def render_video(script, title="AI YouTube Agent"):
    """
    Render a real 1920x1080 MP4 from the generated script.

    This V1 intentionally uses generated educational scene cards rather
    than external AI images. It needs only Pillow + FFmpeg.
    """
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            "FFmpeg was not found on PATH. "
            "Open a new terminal or add C:\\ffmpeg\\bin to PATH."
        )

    sections = script.get("sections", []) if isinstance(script, dict) else []
    if not sections:
        raise RuntimeError("The generated script contains no sections.")

    scene_dir = IMAGES_DIR / "rendered_scenes"
    scene_dir.mkdir(parents=True, exist_ok=True)

    scene_paths = []
    durations = []

    for index, section in enumerate(sections, start=1):
        narration = str(section.get("narration", "")).strip()
        scene_title = str(
            section.get("section_title", f"Scene {index}")
        ).strip()

        # About 130 spoken words/minute, with sensible limits.
        words = max(1, len(narration.split()))
        duration = max(5.0, min(60.0, words / 130.0 * 60.0))

        scene_path = scene_dir / f"scene_{index:02d}.jpg"
        _create_scene_image(
            index,
            scene_title,
            narration,
            scene_path,
        )

        scene_paths.append(scene_path)
        durations.append(duration)

    concat_path = scene_dir / "concat.txt"
    _write_concat_file(scene_paths, durations, concat_path)

    output = FINAL_DIR / "ai_youtube_agent_sample.mp4"

    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-vf",
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
        f"format=yuv420p",
        "-r",
        str(FPS),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "20",
        "-movflags",
        "+faststart",
        str(output),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "FFmpeg failed:\n" + result.stderr[-5000:]
        )

    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("FFmpeg finished but no MP4 was created.")

    return output


def create_video_from_image_and_audio(image, audio, output_name="sample_video.mp4"):
    """Backward-compatible helper retained for the older V1 API."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("FFmpeg was not found on PATH.")

    output = FINAL_DIR / output_name
    cmd = [
        ffmpeg,
        "-y",
        "-loop",
        "1",
        "-i",
        str(image),
        "-i",
        str(audio),
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        str(output),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-3000:])
    return output
