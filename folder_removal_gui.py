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
            "Adobe Premiere Pro Video Previews",
            "Original media",
            "Transcoded media"
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

    def remove_folders(self):
        """Searches for and removes specified folders in the selected directory."""
        if not self.selected_path:
            messagebox.showerror("Error", "Please select a location first.")
            return

        folders_removed = []
        for root_dir, dirs, files in os.walk(self.selected_path):
            for folder_name in dirs:
                if folder_name in self.folders_to_remove:
                    folder_path = os.path.join(root_dir, folder_name)
                    try:
                        shutil.rmtree(folder_path)
                        folders_removed.append(folder_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to remove {folder_path}: {e}")

        if folders_removed:
            self.status_label.config(text="Folders Removed Successfully", fg="green")
            removed_folders = "\n".join(folders_removed)
            messagebox.showinfo("Success", f"Removed the following folders:\n{removed_folders}")
        else:
            self.status_label.config(text="No folders found to remove", fg="blue")
            messagebox.showinfo("Info", "No specified folders were found in the selected location.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FolderRemoverApp(root)
    root.mainloop()
