
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from duplicate_finder import (
    DEFAULT_PHASH_THRESHOLD,
    find_exact_duplicates,
    find_near_duplicates,
)
from scanner import scan_folder


class DuplicateImageFinderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Duplicate Image Finder")
        self.root.geometry("700x420")
        self.root.minsize(560, 350)

        self.selected_folder = tk.StringVar(value="No folder selected")
        self.status = tk.StringVar(value="Select a folder to get started.")
        self.results = tk.StringVar(value="No scan results yet.")

        self._build_ui()

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame,
            text="Duplicate Image Finder",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(0, 20))

        ttk.Label(main_frame, text="Selected folder:").pack(anchor="w")

        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill="x", pady=(5, 15))

        ttk.Label(
            folder_frame,
            textvariable=self.selected_folder,
            wraplength=480,
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            folder_frame,
            text="Browse...",
            command=self.select_folder,
        ).pack(side="right", padx=(10, 0))

        self.scan_button = ttk.Button(
            main_frame,
            text="Scan Images",
            command=self.start_scan,
            state="disabled",
        )
        self.scan_button.pack(anchor="w", pady=(0, 20))

        ttk.Separator(main_frame).pack(fill="x", pady=(0, 20))

        ttk.Label(
            main_frame,
            text="Scan Results",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        ttk.Label(
            main_frame,
            textvariable=self.results,
            justify="left",
            wraplength=620,
        ).pack(anchor="w")

        ttk.Label(
            main_frame,
            textvariable=self.status,
            wraplength=620,
        ).pack(anchor="w", side="bottom", pady=(15, 0))

    def select_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select Image Folder")

        if folder:
            self.selected_folder.set(folder)
            self.scan_button.config(state="normal")
            self.status.set("Folder selected. Ready to scan.")
            self.results.set("No scan results yet.")

    def start_scan(self) -> None:
        folder = self.selected_folder.get()

        if not Path(folder).is_dir():
            messagebox.showerror(
                "Invalid Folder",
                "Please select a valid folder.",
            )
            return

        self.scan_button.config(state="disabled")
        self.status.set("Scanning images. Please wait...")
        self.results.set("Scan in progress...")

        threading.Thread(
            target=self._scan_worker,
            args=(folder,),
            daemon=True,
        ).start()

    def _scan_worker(self, folder: str) -> None:
        try:
            image_files = scan_folder(folder)
            exact_groups = find_exact_duplicates(image_files)
            near_groups = find_near_duplicates(
                image_files,
                threshold=DEFAULT_PHASH_THRESHOLD,
            )

            result_text = (
                f"Images found: {len(image_files)}\n"
                f"Exact duplicate groups: {len(exact_groups)}\n"
                f"Near-duplicate groups: {len(near_groups)}\n"
                f"pHash threshold: {DEFAULT_PHASH_THRESHOLD}"
            )

            self.root.after(
                0,
                lambda: self._scan_complete(result_text),
            )

        except Exception as error:
            self.root.after(
                0,
                lambda error=error: self._scan_failed(error),
            )

    def _scan_complete(self, result_text: str) -> None:
        self.results.set(result_text)
        self.status.set("Scan completed.")
        self.scan_button.config(state="normal")

    def _scan_failed(self, error: Exception) -> None:
        self.status.set("Scan failed.")
        self.scan_button.config(state="normal")

        messagebox.showerror(
            "Scan Error",
            f"An error occurred while scanning:\n{error}",
        )


def run_app() -> None:
    root = tk.Tk()
    DuplicateImageFinderApp(root)
    root.mainloop()