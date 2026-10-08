from scanner import scan_folder
from duplicate_finder import find_exact_duplicates


folder = input("Enter folder path: ")

image_files = scan_folder(folder)

print(f"\nScanned {len(image_files)} image(s).")

duplicate_groups = find_exact_duplicates(image_files)

print(f"Found {len(duplicate_groups)} duplicate group(s).\n")

for index, group in enumerate(duplicate_groups, start=1):
    print(f"Duplicate Group {index}:")

    for file_path in group:
        print(f"  {file_path}")

    print()