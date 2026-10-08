# Duplicate Image Finder

A lightweight desktop application built with Python and Tkinter to find exact duplicates, visually similar images, and corrupted image files in a folder. It helps users organize their image collections and remove unnecessary files.

## Features

* **Recursive Image Scanning** — Scans a selected folder and its subfolders for supported image formats.
* **Exact Duplicate Detection** — Uses SHA-256 hashing to identify files with identical contents.
* **Near-Duplicate Detection** — Uses perceptual hashing (pHash) to identify visually similar images.
* **Corrupted File Detection** — Identifies image files that Pillow cannot verify or open correctly.
* **Separate Results Tabs** — Displays exact duplicates, near duplicates, and corrupted files in separate tabs.
* **Open Image** — Opens a selected image using the operating system's default image viewer.
* **Delete Selected** — Deletes selected files after user confirmation.
* **Automatic Refresh** — Rescans the selected folder after successful deletion.
* **Background Scanning** — Performs scanning in a background thread to keep the interface responsive.
* **Error Handling** — Handles unreadable image files and common file-operation errors.

## Supported Image Formats

* JPG / JPEG
* PNG
* WEBP
* BMP
* GIF
* TIFF

## Tech Stack

* **Python** — Core application logic
* **Tkinter** — Desktop graphical user interface
* **Pillow** — Image loading and verification
* **ImageHash** — Perceptual hashing for near-duplicate detection
* **hashlib** — SHA-256 hashing for exact duplicate detection
* **Threading** — Background scanning

## Project Structure

```text
duplicate-image-finder/
├── main.py
├── scanner.py
├── hasher.py
├── duplicate_finder.py
├── ui/
│   ├── __init__.py
│   └── app.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd duplicate-image-finder
```

Replace `<your-repository-url>` with your GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

From the project root, execute:

```bash
python main.py
```

## How to Use

1. Launch the application.
2. Click **Browse...** and select a folder containing images.
3. Click **Scan Images**.
4. Review the results in the Exact Duplicates, Near Duplicates, and Corrupted Files tabs.
5. Select an image and click **Open Image** to inspect it.
6. Select one or more rows and click **Delete Selected** to remove files.
7. Confirm the deletion. The application automatically rescans the selected folder after successful deletion.

## How Detection Works

### Exact Duplicates

Each image file is processed using SHA-256 hashing. Files with matching hashes are grouped as exact duplicates.

### Near Duplicates

The application calculates perceptual hashes (pHash) and compares their Hamming distance. Images whose distance is within the configured threshold are grouped as near duplicates.

The default pHash threshold is **10**. A higher threshold generally allows more visual differences, while a lower threshold requires images to be more similar.

### Corrupted Files

The application uses Pillow to verify image files. Files that fail verification or cannot be opened are reported in the Corrupted Files tab.

## Safety Notes

* File deletion is permanent and does not move files to the Recycle Bin.
* Review selected files before confirming deletion.
* Test the application on a temporary folder before using it on important image collections.
* Detection results depend on image readability and the configured perceptual-hash threshold.

## Current Limitations

* Near-duplicate detection is based on perceptual-hash distance and may not identify every visually similar image.
* Corrupted-file detection depends on Pillow's ability to open and verify the image.
* The application is designed for local desktop use and does not require a database, cloud service, or hosted backend.

## Future Improvements

* Display image thumbnails in the results.
* Add a configurable pHash threshold in the UI.
* Add a safer option to move deleted files to the Recycle Bin.
* Add progress reporting for large folders.
* Improve near-duplicate grouping and comparison.

## License

MIT License

Copyright (c) [2026] [rakesh paramanick]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
