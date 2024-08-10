import hashlib
import os
import json
import threading
import tkinter as tk
from tkinter import ttk

def calculate_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def load_hashes(hash_file):
    """Loads hashes from a JSON file."""
    try:
        with open(hash_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_hashes(hash_dict, hash_file):
    """Saves hashes to a JSON file."""
    with open(hash_file, 'w') as f:
        json.dump(hash_dict, f, indent=4)

class FileIntegrityChecker:
    def __init__(self, root):
        self.root = root
        self.scan_running = False
        self.hash_file = "hashes.json"

        self.directory_label = tk.Label(root, text="Directory to scan:")
        self.directory_label.pack()

        self.directory_entry = tk.Entry(root)
        self.directory_entry.pack()

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.start_button = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Scan", command=self.stop_scan)
        self.stop_button.pack()

    def start_scan(self):
        if not self.scan_running:
            self.scan_running = True
            self.result_label.config(text="Scanning...")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            scan_thread = threading.Thread(target=self.scan_directory)
            scan_thread.start()

    def stop_scan(self):
        self.scan_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def scan_directory(self):
        directory_to_check = self.directory_entry.get()
        hash_dict = load_hashes(self.hash_file)
        changed_files = []

        total_files = sum(len(files) for _, _, files in os.walk(directory_to_check))
        self.progress_bar['maximum'] = total_files

        for root, _, files in os.walk(directory_to_check):
            if not self.scan_running:
                break
            for file in files:
                if not self.scan_running:
                    break
                filepath = os.path.join(root, file)
                try:
                    new_hash = calculate_hash(filepath)
                    old_hash = hash_dict.get(filepath)
                    if old_hash is None or old_hash != new_hash:
                        changed_files.append(filepath)
                    hash_dict[filepath] = new_hash
                    self.progress_bar['value'] += 1
                    self.root.update_idletasks()
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
                except PermissionError:
                    print(f"Permission denied for: {filepath}")

        save_hashes(hash_dict, self.hash_file)

        if changed_files:
            self.result_label.config(text="Changed files:\n" + "\n".join(changed_files))
        else:
            self.result_label.config(text="No changes detected.")

        self.progress_bar['value'] = 0
        self.scan_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

def create_gui():
    root = tk.Tk()
    root.title("File Integrity Checker")
    FileIntegrityChecker(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()

