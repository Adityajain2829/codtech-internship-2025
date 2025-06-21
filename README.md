# 🛡️ File Integrity Monitor Tool

This Python script monitors changes in files by calculating and comparing their **SHA-256 hash values** to ensure file integrity.

## 🔧 Features

- Detects **added**, **removed**, and **modified** files
- Uses `hashlib` for hashing
- Saves and compares file hashes in `file_hashes.json`
- Simple and lightweight — no external libraries needed

## 🚀 Getting Started

### Prerequisites
- Python 3.x

### Installation
Clone the repository:
```bash
git clone https://github.com/Adityajain2829/file-integrity-monitor.git
cd file-integrity-monitor
```

### Usage
```bash
python file_integrity_monitor.py
```
Enter the directory path when prompted, and the script will:
- Scan and store hashes on the first run
- Detect changes in subsequent runs

## 📄 License
This project is licensed under the [MIT License](LICENSE).
