
from pathlib import Path

from hasher import calculate_phash


folder = Path(input("Enter image folder path: ").strip().strip('"'))

for file_path in folder.iterdir():
    if not file_path.is_file():
        continue

    try:
        phash = calculate_phash(file_path)
        print(f"{file_path.name} -> {phash}")
    except Exception as error:
        print(f"Skipped {file_path.name}: {error}")