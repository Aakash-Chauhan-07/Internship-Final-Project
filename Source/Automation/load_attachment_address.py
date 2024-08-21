import tkinter as tk
from tkinter import filedialog
import ctypes

def load_attachment_address():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # Create a root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog for multiple file selections
    file_paths = filedialog.askopenfilenames()

    return file_paths

if __name__ == "__main__":
    file_paths = load_attachment_address()
    print(file_paths)  # Print the selected file paths
