# Python Cybersecurity Toolkit MVP

## Overview

This MVP (Minimum Viable Product) combines multiple beginner-friendly cybersecurity and networking tools into one organized Python project.

The toolkit includes:

1. AES-256 File Encryptor
2. File Integrity Monitor
3. Port Scanner
4. Web Security Header Scanner

These projects are suitable for:

* GitHub portfolio
* Internship applications
* Cybersecurity learning
* Networking fundamentals
* Python practice

---

# Recommended Project Structure

```text
cybersecurity-toolkit/
│
├── README.md
├── requirements.txt
├── main.py
│
├── encryption/
│   └── aes_encryptor.py
│
├── integrity/
│   └── file_integrity_monitor.py
│
├── networking/
│   └── port_scanner.py
│
├── web_security/
│   └── security_header_scanner.py
│
└── screenshots/
```

---

# requirements.txt

```txt
pycryptodome
requests
colorama
```

---

# 1. AES-256 File Encryptor

## Features

* AES-256 encryption
* AES-256 decryption
* Password-based encryption
* GUI support
* Secure file handling

## aes_encryptor.py

```python
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100000


def generate_key(password, salt):
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)


def encrypt_file(filepath, password):
    try:
        salt = get_random_bytes(SALT_SIZE)
        key = generate_key(password.encode(), salt)

        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv

        with open(filepath, 'rb') as f:
            plaintext = f.read()

        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        output_path = filepath + '.enc'

        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(iv)
            f.write(ciphertext)

        messagebox.showinfo('Success', 'File encrypted successfully')

    except Exception as e:
        messagebox.showerror('Error', str(e))


def decrypt_file(filepath, password):
    try:
        with open(filepath, 'rb') as f:
            salt = f.read(SALT_SIZE)
            iv = f.read(16)
            ciphertext = f.read()

        key = generate_key(password.encode(), salt)

        cipher = AES.new(key, AES.MODE_CBC, iv)

        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        output_path = filepath.replace('.enc', '_decrypted')

        with open(output_path, 'wb') as f:
            f.write(plaintext)

        messagebox.showinfo('Success', 'File decrypted successfully')

    except Exception:
        messagebox.showerror('Error', 'Wrong password or corrupted file')


def browse_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)


def encrypt_action():
    path = file_entry.get()
    password = password_entry.get()

    if path and password:
        encrypt_file(path, password)


def decrypt_action():
    path = file_entry.get()
    password = password_entry.get()

    if path and password:
        decrypt_file(path, password)


root = tk.Tk()
root.title('AES-256 File Encryptor')
root.geometry('500x200')


tk.Label(root, text='File').pack(pady=5)

file_entry = tk.Entry(root, width=60)
file_entry.pack()


tk.Button(root, text='Browse', command=browse_file).pack(pady=5)


tk.Label(root, text='Password').pack()

password_entry = tk.Entry(root, show='*', width=60)
password_entry.pack()


tk.Button(root, text='Encrypt', command=encrypt_action).pack(pady=10)

tk.Button(root, text='Decrypt', command=decrypt_action).pack()

root.mainloop()
```

---

# 2. File Integrity Monitor

## Features

* Detects modified files
* Detects deleted files
* Detects added files
* Uses SHA-256 hashing

## file_integrity_monitor.py

```python
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
```

---

# 3. Port Scanner

## Features

* TCP port scanning
* Multi-threaded scanning
* Service detection
* Hostname support

## port_scanner.py

```python
import socket
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    80: 'HTTP',
    443: 'HTTPS'
}


def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)

            result = sock.connect_ex((target, port))

            if result == 0:
                service = COMMON_PORTS.get(port, 'Unknown')
                print(f'[+] Port {port} OPEN ({service})')

    except Exception:
        pass


def main():
    target = input('Enter target IP or hostname: ')

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print('Invalid hostname.')
        return

    print(f'Scanning {target} ({target_ip})...')

    ports = range(1, 1025)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda p: scan_port(target_ip, p), ports)


if __name__ == '__main__':
    main()
```

---

# 4. Web Security Header Scanner

## Features

* Checks security headers
* HTTPS verification
* Basic web security auditing

## security_header_scanner.py

```python
import requests


def check_security(url):
    try:
        response = requests.get(url, timeout=5)

        print('Status Code:', response.status_code)

        headers = response.headers

        security_headers = [
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Content-Security-Policy'
        ]

        print('\nSecurity Headers:')

        for header in security_headers:
            if header in headers:
                print(f'[+] {header} found')
            else:
                print(f'[-] {header} missing')

        if url.startswith('https://'):
            print('\n[+] HTTPS enabled')
        else:
            print('\n[-] HTTPS not enabled')

    except Exception as e:
        print('Error:', e)


if __name__ == '__main__':
    target = input('Enter website URL: ')
    check_security(target)
```

---

# Main Launcher (Optional)

## main.py

```python
import os

while True:
    print('\n=== Cybersecurity Toolkit ===')
    print('1. AES File Encryptor')
    print('2. File Integrity Monitor')
    print('3. Port Scanner')
    print('4. Security Header Scanner')
    print('5. Exit')

    choice = input('Select option: ')

    if choice == '1':
        os.system('python encryption/aes_encryptor.py')

    elif choice == '2':
        os.system('python integrity/file_integrity_monitor.py')

    elif choice == '3':
        os.system('python networking/port_scanner.py')

    elif choice == '4':
        os.system('python web_security/security_header_scanner.py')

    elif choice == '5':
        break

    else:
        print('Invalid choice')
```

---

# Recommended GitHub Repository Name

```text
python-cybersecurity-toolkit
```

---

# Skills Demonstrated

* Python Programming
* Cybersecurity Basics
* Cryptography
* Networking
* File Handling
* GUI Development
* SHA-256 Hashing
* Socket Programming
* Web Security

---

# Future Improvements

You can later add:

* GUI Dashboard
* Dark Mode
* Malware Hash Checker
* Real-time Monitoring
* Report Exporting
* Logging System
* Database Integration
* Email Alerts
* Packet Sniffer
* Network Analyzer

---

# Portfolio Value

This MVP is suitable for:

* Internship applications
* GitHub portfolio
* Resume projects
* Cybersecurity learning
* Networking practice
* Python development practice

It demonstrates both programming and security fundamentals in an ethical and practical way.
