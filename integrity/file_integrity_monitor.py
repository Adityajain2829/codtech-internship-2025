import os
import hashlib
import json

HASH_DB = 'hashes.json'


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_directory(directory):
    hashes = {}

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            try:
                hashes[path] = calculate_hash(path)
            except Exception as e:
                print(f'Error: {e}')

    return hashes


def save_hashes(hashes):
    with open(HASH_DB, 'w') as f:
        json.dump(hashes, f, indent=4)


def load_hashes():
    if not os.path.exists(HASH_DB):
        return {}

    with open(HASH_DB, 'r') as f:
        return json.load(f)


def compare_hashes(old, new):
    old_files = set(old)
    new_files = set(new)

    print('\nAdded Files:')
    for f in new_files - old_files:
        print(f'+ {f}')

    print('\nRemoved Files:')
    for f in old_files - new_files:
        print(f'- {f}')

    print('\nModified Files:')
    for f in old_files & new_files:
        if old[f] != new[f]:
            print(f'* {f}')


if __name__ == '__main__':
    directory = input('Enter directory to monitor: ')

    if not os.path.exists(HASH_DB):
        hashes = scan_directory(directory)
        save_hashes(hashes)
        print('Baseline hashes saved.')

    else:
        old_hashes = load_hashes()
        new_hashes = scan_directory(directory)
        compare_hashes(old_hashes, new_hashes)
