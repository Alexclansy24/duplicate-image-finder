from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tiff",
}


def scan_folder(folder_path: str) -> list[Path]:
    """
    Recursively scan a folder and return all supported image files.
    """

    folder = Path(folder_path)

    if not folder.is_dir():
        raise ValueError(f"Invalid folder path: {folder_path}")

    image_files = []

    for file_path in folder.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            image_files.append(file_path)

    return image_files