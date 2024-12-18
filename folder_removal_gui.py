import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class FolderRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Remover App")
        self.root.geometry("400x200")

        # List of folders to be removed
        self.folders_to_remove = [
            "Original Media",
            "Render Files",
            "Transcoded Media",
            "Final Cut Original Media",
            "Final Cut Optimized Media",
            "Adobe Premiere Pro Video Previews"
        ]

        # GUI Elements
        self.label = tk.Label(root, text="Select the location to search for specific folders to remove")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Location", command=self.select_location)
        self.select_button.pack(pady=5)

        self.run_button = tk.Button(root, text="Remove Folders", command=self.remove_folders, state=tk.DISABLED)
        self.run_button.pack(pady=5)

        self.status_label = tk.Label(root, text="Status: Awaiting action", fg="blue")
        self.status_label.pack(pady=10)

        self.selected_path = None

    def select_location(self):
        """Opens a file dialog to select the directory to search in."""
        self.selected_path = filedialog.askdirectory()
        if self.selected_path:
            self.status_label.config(text=f"Selected Path: {self.selected_path}", fg="green")
            self.run_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="No path selected", fg="red")

    def search_packages(self, directory):
        """Recursively searches for folders within packages (files that behave like directories)."""
        for root_dir, dirs, files in os.walk(directory):
            for item in dirs:
                if item.endswith(".fcpbundle") or item.endswith(".pkg") or item.endswith(".app"):
                    package_path = os.path.join(root_dir, item)
                    for inner_root, inner_dirs, _ in os.walk(package_path):
                        for folder_name in inner_dirs:
                            if folder_name in self.folders_to_remove:
                                folder_path = os.path.join(inner_root, folder_name)
                                try:
                                    shutil.rmtree(folder_path)
                                    self.removed_folders.append(folder_path)
                                except Exception:
                                    pass  # Silently handle errors

    def remove_folders(self):
        """Searches for and removes specified folders in the selected directory and inside packages."""
        if not self.selected_path:
            messagebox.showerror("Error", "Please select a location first.")
            return

        self.removed_folders = []

        # Search for specified folders in the selected path
        for root_dir, dirs, files in os.walk(self.selected_path):
            for folder_name in dirs:
                if folder_name in self.folders_to_remove:
                    folder_path = os.path.join(root_dir, folder_name)
                    try:
                        shutil.rmtree(folder_path)
                        self.removed_folders.append(folder_path)
                    except Exception:
                        pass  # Silently handle errors
        
        # Search inside .fcpbundle, .app, and .pkg packages
        self.search_packages(self.selected_path)

        self.status_label.config(text="Folders Removal Process Completed", fg="green")
        messagebox.showinfo("Done", "Folders removal process is complete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderRemoverApp(root)
    root.mainloop()
