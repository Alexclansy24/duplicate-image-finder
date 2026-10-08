
from pathlib import Path
import imagehash
from hasher import calculate_phash, calculate_sha256


DEFAULT_PHASH_THRESHOLD = 10


def find_exact_duplicates(image_files: list[Path]) -> list[list[Path]]:
    """Group files with identical SHA-256 hashes."""

    hash_groups: dict[str, list[Path]] = {}

    for file_path in image_files:
        try:
            file_hash = calculate_sha256(file_path)
        except OSError as error:
            print(f"Skipped {file_path}: {error}")
            continue

        hash_groups.setdefault(file_hash, []).append(file_path)

    return [
        files
        for files in hash_groups.values()
        if len(files) > 1
    ]


def find_near_duplicates(
    image_files: list[Path],
    threshold: int = DEFAULT_PHASH_THRESHOLD,
) -> list[list[Path]]:
    """Group visually similar images using perceptual hash distance."""

    if not 0 <= threshold <= 64:
        raise ValueError("Threshold must be between 0 and 64.")

    phash_groups: dict[Path, imagehash.ImageHash] = {}

    for file_path in image_files:
        try:
            phash_groups[file_path] = calculate_phash(file_path)
        except (OSError, ValueError) as error:
            print(f"Skipped {file_path}: {error}")

    remaining = set(phash_groups)
    duplicate_groups: list[list[Path]] = []

    while remaining:
        first = remaining.pop()
        group = [first]

        for candidate in list(remaining):
            distance = phash_groups[first] - phash_groups[candidate]

            if distance <= threshold:
                group.append(candidate)
                remaining.remove(candidate)

        if len(group) > 1:
            duplicate_groups.append(sorted(group))

    return duplicate_groups