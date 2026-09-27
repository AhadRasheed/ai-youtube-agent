from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import THUMBNAILS_DIR


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


def create_thumbnail(title):
    """Create a simple real 1280x720 PNG thumbnail."""
    width, height = 1280, 720
    image = Image.new("RGB", (width, height), (18, 22, 32))
    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (40, 40, width - 40, height - 40),
        outline=(80, 180, 255),
        width=6,
    )

    title = title.strip() or "AI YouTube Video"

    # Keep the sample thumbnail readable.
    if len(title) > 55:
        title = title[:52] + "..."

    bbox = draw.multiline_textbbox(
        (0, 0),
        title,
        font=_font(64, bold=True),
        spacing=12,
    )
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    draw.multiline_text(
        ((width - tw) / 2, (height - th) / 2),
        title,
        font=_font(64, bold=True),
        fill=(245, 248, 255),
        align="center",
        spacing=12,
    )

    path = THUMBNAILS_DIR / "thumbnail.png"
    image.save(path, "PNG")

    # Also keep a text copy for debugging.
    (THUMBNAILS_DIR / "thumbnail.txt").write_text(
        title,
        encoding="utf-8",
    )
    return path
