import hashlib
from pathlib import Path

import imagehash
from PIL import Image


def calculate_sha256(file_path: Path) -> str:
    """
    Calculate the SHA-256 hash of a file.
    """

    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()

def calculate_phash(file_path: Path) -> imagehash.ImageHash:
    """Generate a perceptual hash for an image."""

    with Image.open(file_path) as image:
        return imagehash.phash(image)