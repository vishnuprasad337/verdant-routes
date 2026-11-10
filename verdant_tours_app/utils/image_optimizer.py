from pathlib import Path

from PIL import Image


def optimize_image(path: str, max_size: tuple[int, int] = (1200, 1200), quality: int = 70) -> None:
    """Optimize an image in place if it exists on disk."""
    image_path = Path(path)
    if not image_path.exists():
        return

    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail(max_size)
            img.save(image_path, quality=quality, optimize=True)
    except Exception:
        # Keep model save resilient even if optimization fails.
        return
