
from pathlib import Path

from hasher import calculate_phash


image1 = Path(
    r"c:\Users\clans\Downloads\test2"
    r"\ertwt2.webp"
)

image2 = Path(
    r"c:\Users\clans\Downloads\test2\ertwt.jpg"
)

hash1 = calculate_phash(image1)
hash2 = calculate_phash(image2)

distance = hash1 - hash2

print(f"Image 1 pHash: {hash1}")
print(f"Image 2 pHash: {hash2}")
print(f"Hamming distance: {distance}")
print(f"Detected at threshold 5: {distance <= 5}")