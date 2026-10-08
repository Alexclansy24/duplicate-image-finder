
from scanner import scan_folder
from duplicate_finder import find_near_duplicates


folder = input("Enter folder path: ").strip().strip('"')
image_files = scan_folder(folder)

print(f"\nScanned {len(image_files)} image(s).")

groups = find_near_duplicates(image_files, threshold=10)

print(f"Found {len(groups)} near-duplicate group(s).\n")

for index, group in enumerate(groups, start=1):
    print(f"Near-Duplicate Group {index}:")

    for file_path in group:
        print(f"  {file_path}")

    print()