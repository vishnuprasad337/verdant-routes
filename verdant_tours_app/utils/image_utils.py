"""
image_utils.py

- Converts any uploaded image (JPG / PNG / etc.) to WebP
- Keeps the file near 150 KB (lowers quality first, then size)
- Creates smaller copies for srcset (480w, 768w, 1200w)
- Keeps PNG transparency
- Fixes phone photos that are rotated (EXIF)

Needs: Pillow (the normal pip wheel already supports WebP)
"""

import io
from pathlib import Path, PurePosixPath

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

# ------------------------------------------------------------------
# SETTINGS (change here only)
# ------------------------------------------------------------------
TARGET_KB = 150                  # target file size of the main image
MAX_DIMENSION = 1600             # longest side of the main image (px)
SRCSET_WIDTHS = (480, 768, 1200) # extra sizes made for srcset
MIN_QUALITY = 40
MAX_QUALITY = 85
SKIP_EXTENSIONS = (".svg", ".gif")   # left untouched


# ------------------------------------------------------------------
# CORE: Pillow image -> WebP bytes (about TARGET_KB)
# ------------------------------------------------------------------
def _prepare(img):
    """Fix rotation and colour mode (keeps transparency)."""
    img = ImageOps.exif_transpose(img)
    has_alpha = img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info
    )
    return img.convert("RGBA" if has_alpha else "RGB")


def _best_quality(img, target_bytes):
    """Highest WebP quality that still fits in target_bytes (or None)."""
    low, high, best = MIN_QUALITY, MAX_QUALITY, None

    while low <= high:
        mid = (low + high) // 2
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=mid, method=4)

        if buf.tell() <= target_bytes:
            best, low = buf, mid + 1
        else:
            high = mid - 1

    return best


def make_webp_bytes(img, target_kb=TARGET_KB, max_dimension=MAX_DIMENSION):
    img = _prepare(img)
    img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
    target_bytes = target_kb * 1024

    while True:
        buf = _best_quality(img, target_bytes)
        if buf is not None:
            return buf.getvalue()

        width, height = img.size

        # very small already: accept the lowest quality
        if max(width, height) <= 400:
            buf = io.BytesIO()
            img.save(buf, "WEBP", quality=MIN_QUALITY, method=4)
            return buf.getvalue()

        # still too big: make the picture 10% smaller and try again
        img = img.resize((int(width * 0.9), int(height * 0.9)), Image.LANCZOS)


def convert_to_webp(file_obj, name=None):
    """Uploaded file -> ContentFile (.webp)"""
    file_obj.seek(0)
    with Image.open(file_obj) as img:
        data = make_webp_bytes(img)

    stem = Path(name or file_obj.name).stem
    return ContentFile(data, name=f"{stem}.webp")


# ------------------------------------------------------------------
# SRCSET VARIANTS: photo.webp -> photo-480w.webp, photo-768w.webp ...
# ------------------------------------------------------------------
def _variant_name(name, width):
    path = PurePosixPath(Path(name).as_posix())
    return path.with_name(f"{path.stem}-{width}w.webp").as_posix()


def create_srcset_variants(field_file, widths=SRCSET_WIDTHS):
    storage = field_file.storage

    with storage.open(field_file.name) as f:
        img = Image.open(f)
        img.load()

    for width in widths:
        if width >= img.width:
            continue

        height = max(1, int(img.height * width / img.width))
        small = img.resize((width, height), Image.LANCZOS)
        data = make_webp_bytes(small, max_dimension=width)

        name = _variant_name(field_file.name, width)
        if storage.exists(name):
            storage.delete(name)
        storage.save(name, ContentFile(data))


def build_srcset(field_file, widths=SRCSET_WIDTHS):
    """String for the srcset="" attribute."""
    if not field_file:
        return ""

    storage = field_file.storage
    parts = []

    for width in widths:
        name = _variant_name(field_file.name, width)
        if storage.exists(name):
            parts.append(f"{storage.url(name)} {width}w")

    try:
        parts.append(f"{field_file.url} {field_file.width}w")
    except Exception:
        pass

    return ", ".join(parts)


# ------------------------------------------------------------------
# MAIN ENTRY: call inside Model.save() before super().save()
# ------------------------------------------------------------------
def optimize_image_field(instance, field_name="image"):
    """
    Converts a NEWLY uploaded image to WebP (~150 KB) and makes the
    srcset copies. Images that are already saved are not touched again.
    """
    field = getattr(instance, field_name, None)

    if not field or getattr(field, "_committed", True):
        return False                      # nothing new was uploaded

    if Path(field.name).suffix.lower() in SKIP_EXTENSIONS:
        return False

    try:
        webp = convert_to_webp(field.file, field.name)
    except Exception:
        return False                      # keep saving even if it fails

    field.save(webp.name, webp, save=False)

    try:
        create_srcset_variants(field)
    except Exception:
        pass

    return True