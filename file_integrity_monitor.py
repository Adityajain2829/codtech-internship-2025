import os
import hashlib
import json
import argparse

HASH_DB = "file_hashes.json"

def calculate_file_hash(file_path, algorithm="sha256"):
    """Calculate the hash of a file."""
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def scan_directory(directory, algorithm="sha256"):
    """Scan directory and calculate hashes for all files."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                file_hashes[file_path] = calculate_file_hash(file_path, algorithm)
            except Exception as e:
                print(f"Error hashing {file_path}: {e}")
    return file_hashes

def load_hashes(db_path=HASH_DB):
    if not os.path.exists(db_path):
        return {}
    with open(db_path, "r") as f:
        return json.load(f)

def save_hashes(hashes, db_path=HASH_DB):
    with open(db_path, "w") as f:
        json.dump(hashes, f, indent=4)

def compare_hashes(old_hashes, new_hashes):
    """Compare old and new hash dictionaries."""
    added = []
    removed = []
    changed = []

    old_files = set(old_hashes)
    new_files = set(new_hashes)

    for file in new_files - old_files:
        added.append(file)
    for file in old_files - new_files:
        removed.append(file)
    for file in new_files & old_files:
        if old_hashes[file] != new_hashes[file]:
            changed.append(file)

    return added, removed, changed

def main():
    parser = argparse.ArgumentParser(description="Monitor file changes by hash comparison.")
    parser.add_argument("directory", help="Directory to monitor")
    parser.add_argument("--init", action="store_true", help="Initialize hash database")
    parser.add_argument("--algorithm", choices=hashlib.algorithms_available, default="sha256", help="Hash algorithm to use")
    args = parser.parse_args()

    if args.init:
        print(f"Initializing hash database for {args.directory}...")
        hashes = scan_directory(args.directory, args.algorithm)
        save_hashes(hashes)
        print("Initialization complete. Hash database saved.")
    else:
        print(f"Checking file integrity in {args.directory}...")
        old_hashes = load_hashes()
        new_hashes = scan_directory(args.directory, args.algorithm)
        added, removed, changed = compare_hashes(old_hashes, new_hashes)

        if not (added or removed or changed):
            print("No file changes detected. All files are intact.")
        else:
            if added:
                print("Added files:")
                for f in added:
                    print(f"  + {f}")
            if removed:
                print("Removed files:")
                for f in removed:
                    print(f"  - {f}")
            if changed:
                print("Modified files:")
                for f in changed:
                    print(f"  * {f}")

if __name__ == "__main__":
    main()