from pathlib import Path

from hasher import calculate_sha256


def find_exact_duplicates(image_files: list[Path]) -> list[list[Path]]:
    """
    Find groups of files that have identical SHA-256 hashes.
    """

    hash_groups: dict[str, list[Path]] = {}

    for file_path in image_files:
        file_hash = calculate_sha256(file_path)

        hash_groups.setdefault(file_hash, []).append(file_path)

    duplicate_groups = [
        files
        for files in hash_groups.values()
        if len(files) > 1
    ]

    return duplicate_groups