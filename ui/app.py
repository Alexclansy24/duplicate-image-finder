
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from duplicate_finder import (
    DEFAULT_PHASH_THRESHOLD,
    find_corrupted_images,
    find_exact_duplicates,
    find_near_duplicates,
)
from scanner import scan_folder


class DuplicateImageFinderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Duplicate Image Finder")
        self.root.geometry("1000x650")
        self.root.minsize(700, 450)

        self.selected_folder = tk.StringVar(value="No folder selected")
        self.status = tk.StringVar(value="Select a folder to get started.")
        self.summary = tk.StringVar(value="No scan results yet.")
        self.is_scanning = False
        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Duplicate Image Finder",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(0, 15))

        folder_frame = ttk.Frame(main)
        folder_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            folder_frame,
            textvariable=self.selected_folder,
            wraplength=700,
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            folder_frame,
            text="Browse...",
            command=self.select_folder,
        ).pack(side="right", padx=(10, 0))

        self.scan_button = ttk.Button(
            main,
            text="Scan Images",
            command=self.start_scan,
            state="disabled",
        )
        self.scan_button.pack(anchor="w", pady=(0, 12))

        ttk.Label(
            main,
            textvariable=self.summary,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        self.tabs = ttk.Notebook(main)
        self.tabs.pack(fill="both", expand=True)

        self.exact_tree = self._create_results_tab(
            "Exact Duplicates"
        )
        self.near_tree = self._create_results_tab(
            "Near Duplicates"
        )
        self.corrupted_tree = self._create_results_tab(
        "Corrupted Files"
        )
        
        delete_frame = ttk.Frame(main)
        delete_frame.pack(fill="x", pady=(10, 0))

        
        ttk.Button(
            delete_frame,
            text="Open Image",
            command=self.open_selected_image,
        ).pack(side="left", padx=(10, 0))

        ttk.Button(
            delete_frame,
            text="Delete Selected",
            command=self.delete_selected,
        ).pack(side="left")

        ttk.Label(
            delete_frame,
            text="Select image rows in either tab before deleting.",
        ).pack(side="left", padx=(12, 0))

        ttk.Label(
            main,
            textvariable=self.status,
        ).pack(anchor="w", pady=(10, 0))

    def _create_results_tab(self, title: str) -> ttk.Treeview:
        tab = ttk.Frame(self.tabs, padding=5)
        self.tabs.add(tab, text=title)

        columns = ("group", "filename", "path")
        tree = ttk.Treeview(
            tab,
            columns=columns,
            show="headings",
            selectmode="extended",
        )

        tree.heading("group", text="Group")
        tree.heading("filename", text="Filename")
        tree.heading("path", text="Full Path")

        tree.column("group", width=90, stretch=False)
        tree.column("filename", width=240, stretch=True)
        tree.column("path", width=520, stretch=True)

        vertical_scroll = ttk.Scrollbar(
            tab,
            orient="vertical",
            command=tree.yview,
        )
        horizontal_scroll = ttk.Scrollbar(
            tab,
            orient="horizontal",
            command=tree.xview,
        )

        tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)

        return tree

    def select_folder(self) -> None:
        folder = filedialog.askdirectory(
            title="Select Image Folder"
        )

        if folder:
            self.selected_folder.set(folder)
            self.scan_button.config(state="normal")
            self.status.set("Folder selected. Ready to scan.")
            self.summary.set("No scan results yet.")
            self._clear_results()

    def _clear_results(self) -> None:
        for tree in (self.exact_tree, self.near_tree, self.corrupted_tree):
            tree.delete(*tree.get_children())

    def start_scan(self) -> None:
        if self.is_scanning:
            return
        self.is_scanning = True
        folder = self.selected_folder.get()

        if not Path(folder).is_dir():
            messagebox.showerror(
                "Invalid Folder",
                "Please select a valid folder.",
            )
            return

        self.scan_button.config(state="disabled")
        self.status.set("Scanning images. Please wait...")
        self.summary.set("Scan in progress...")
        self._clear_results()

        threading.Thread(
            target=self._scan_worker,
            args=(folder,),
            daemon=True,
        ).start()

    
    def _scan_worker(self, folder: str) -> None:
        try:
            image_files = scan_folder(folder)
            corrupted_files = find_corrupted_images(image_files)
            valid_images = [
                file_path
                for file_path in image_files
                if file_path not in set(corrupted_files)
            ]
            exact_groups = find_exact_duplicates(valid_images)

            near_groups = find_near_duplicates(
                valid_images,
                threshold=DEFAULT_PHASH_THRESHOLD,
            )

            # Collect files already identified as exact duplicates.
            exact_files = {
                file_path
                for group in exact_groups
                for file_path in group
            }

            # Exclude exact-duplicate files from near-duplicate results.
            filtered_near_groups = [
                [
                    file_path
                    for file_path in group
                    if file_path not in exact_files
                ]
                for group in near_groups
            ]

            # Keep only groups containing at least two remaining files.
            filtered_near_groups = [
                group
                for group in filtered_near_groups
                if len(group) > 1
            ]

            self.root.after(
                0,
                lambda: self._display_results(
                    len(image_files),
                    exact_groups,
                    filtered_near_groups,
                    corrupted_files,
                ),
            )

        except Exception as error:
            self.root.after(
                0,
                lambda error=error: self._scan_failed(error),
            )
    def _display_group(
        self,
        tree: ttk.Treeview,
        groups: list[list[Path]],
    ) -> None:
        for group_number, group in enumerate(groups, start=1):
            for file_path in sorted(group):
                tree.insert(
                    "",
                    "end",
                    values=(
                        f"Group {group_number}",
                        file_path.name,
                        str(file_path),
                    ),
                )

    def _display_results(
        self,
        image_count: int,
        exact_groups: list[list[Path]],
        near_groups: list[list[Path]],
        corrupted_files: list[Path],
    ) -> None:
        self._display_group(self.exact_tree, exact_groups)
        self._display_group(self.near_tree, near_groups)
        for file_path in sorted(corrupted_files):
            self.corrupted_tree.insert(
                "",
                "end",
                values=(
                    "Corrupted",
                    file_path.name,
                    str(file_path),
                ),
            )

        self.summary.set(
            f"Images scanned: {image_count}\n"
            f"Exact duplicate groups: {len(exact_groups)}\n"
            f"Near-duplicate groups: {len(near_groups)}\n"
            f"Corrupted files: {len(corrupted_files)}\n"
            f"pHash threshold: {DEFAULT_PHASH_THRESHOLD}"
        )

        self.status.set("Scan completed.")
        self.is_scanning = False
        self.scan_button.config(state="normal")

    def _scan_failed(self, error: Exception) -> None:
        self.status.set("Scan failed.")
        self.is_scanning = False
        self.scan_button.config(state="normal")

        messagebox.showerror(
            "Scan Error",
            f"An error occurred while scanning:\n{error}",
        )

    def delete_selected(self) -> None:
        selected_tab = self.tabs.index(self.tabs.select())
        tree = (
            self.exact_tree,
            self.near_tree,
            self.corrupted_tree,
        )[selected_tab]
        selected_items = tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "Nothing Selected",
                "Please select one or more images to delete.",
            )
            return

        selected_paths = [
            Path(tree.item(item, "values")[2])
            for item in selected_items
            if len(tree.item(item, "values")) >= 3
        ]

        if not selected_paths:
            return

        confirmed = messagebox.askyesno(
            "Confirm Deletion",
            f"Permanently delete {len(selected_paths)} selected image(s)?\n\n"
            "This action cannot be undone.",
        )

        if not confirmed:
            return

        deleted_count = 0
        failed_paths = []

        for file_path in selected_paths:
            try:
                file_path.unlink()
                deleted_count += 1
            except OSError:
                failed_paths.append(file_path)

        if deleted_count:
            self.status.set(
                f"Deleted {deleted_count} image(s). Refreshing results..."
            )
            self.start_scan()
        else:
            self.status.set("No images were deleted.")

        if failed_paths:
            messagebox.showwarning(
                "Some Files Could Not Be Deleted",
                f"Deleted: {deleted_count}\n"
                f"Failed: {len(failed_paths)}",
            )

    
    def open_selected_image(self) -> None:
        selected_tab = self.tabs.index(self.tabs.select())
        tree = (
            self.exact_tree,
            self.near_tree,
            self.corrupted_tree,
        )[selected_tab]
        selected_items = tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "Nothing Selected",
                "Please select an image to open.",
            )
            return

        values = tree.item(selected_items[0], "values")

        if len(values) < 3:
            return

        image_path = Path(values[2])

        if not image_path.is_file():
            messagebox.showerror(
                "Image Not Found",
                f"This image no longer exists:\n{image_path}",
            )
            return

        try:
            import os
            import subprocess
            import sys

            if sys.platform == "win32":
                os.startfile(str(image_path))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(image_path)])
            else:
                subprocess.Popen(["xdg-open", str(image_path)])

        except OSError as error:
            messagebox.showerror(
                "Unable to Open Image",
                f"Could not open the image:\n{error}",
            )

def run_app() -> None:
    root = tk.Tk()
    DuplicateImageFinderApp(root)
    root.mainloop()