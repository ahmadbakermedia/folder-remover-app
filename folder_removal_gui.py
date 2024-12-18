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

    def search_fcpbundle(self, directory):
        """Recursively searches for .fcpbundle files and their contents."""
        for root_dir, dirs, files in os.walk(directory):
            for item in dirs:
                if item.endswith(".fcpbundle"):
                    bundle_path = os.path.join(root_dir, item)
                    for inner_root, inner_dirs, _ in os.walk(bundle_path):
                        for folder_name in inner_dirs:
                            if folder_name in self.folders_to_remove:
                                folder_path = os.path.join(inner_root, folder_name)
                                try:
                                    shutil.rmtree(folder_path)
                                    self.removed_folders.append(folder_path)
                                except Exception as e:
                                    messagebox.showerror("Error", f"Failed to remove {folder_path}: {e}")

    def remove_folders(self):
        """Searches for and removes specified folders in the selected directory and inside .fcpbundle files."""
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
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to remove {folder_path}: {e}")
        
        # Search inside .fcpbundle files
        self.search_fcpbundle(self.selected_path)

        if self.removed_folders:
            self.status_label.config(text="Folders Removed Successfully", fg="green")
            removed_folders_str = "\n".join(self.removed_folders)
            messagebox.showinfo("Success", f"Removed the following folders:\n{removed_folders_str}")
        else:
            self.status_label.config(text="No folders found to remove", fg="blue")
            messagebox.showinfo("Info", "No specified folders were found in the selected location or inside .fcpbundle files.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderRemoverApp(root)
    root.mainloop()
