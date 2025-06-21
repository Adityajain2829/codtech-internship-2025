# 🔍 Web Vulnerability Scanner

This Python-based tool scans a web page for **XSS (Cross-Site Scripting)** vulnerabilities by analyzing and testing forms.

## 🚀 Features

- Detects XSS vulnerabilities via form injection
- Uses `requests` and `BeautifulSoup` libraries
- Follows form actions (GET/POST) and tests inputs
- Simple terminal-based interface

## 📦 Requirements

- Python 3.x
- `requests`, `beautifulsoup4`

Install with:
```bash
pip install requests beautifulsoup4
```

## 🔧 Usage

```bash
python web_vuln_scanner.py
```

Then enter a URL like:
```
http://example.com
```

## 📄 License
This project is licensed under the [MIT License](LICENSE).