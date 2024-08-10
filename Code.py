import hashlib
import os
import time
import json

def calculate_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    # ... (your existing function)

def check_directory(directory, hash_dict):
    """Recursively checks files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                new_hash = calculate_hash(filepath)
                old_hash = hash_dict.get(filepath)
                if old_hash is None or old_hash != new_hash:
                    print(f"File changed: {filepath}")
                hash_dict[filepath] = new_hash
            except FileNotFoundError:
                print(f"File not found: {filepath}")
            except PermissionError:
                print(f"Permission denied for: {filepath}")

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

def main(hash_file="hashes.json", check_interval=60):
    hash_dict = load_hashes(hash_file)
    directory_to_check = "path/to/your/directory"  # Replace with the actual directory

    while True:
        check_directory(directory_to_check, hash_dict)
        save_hashes(hash_dict, hash_file)
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
