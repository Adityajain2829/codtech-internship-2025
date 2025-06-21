import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_forms(url):
    """Find all form tags on a page"""
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Extract useful form details"""
    details = {"action": form.attrs.get("action"), "method": form.attrs.get("method", "get").lower(), "inputs": []}
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        details["inputs"].append({"type": input_type, "name": input_name})
    return details

def is_vulnerable_to_xss(response):
    """Basic XSS test"""
    return "<script>alert('xss')</script>" in response.text

def scan_xss(url):
    """Scan URL for XSS vulnerabilities"""
    forms = find_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = "<script>alert('xss')</script>"
    for form in forms:
        details = get_form_details(form)
        data = {}
        for input in details["inputs"]:
            if input["type"] == "text" or input["type"] == "search":
                data[input["name"]] = js_script
        target_url = urljoin(url, details["action"])
        if details["method"] == "post":
            res = requests.post(target_url, data=data)
        else:
            res = requests.get(target_url, params=data)
        if is_vulnerable_to_xss(res):
            print(f"[!] XSS vulnerability detected on {target_url}")
        else:
            print(f"[-] No XSS vulnerability detected on {target_url}")

def main():
    url = input("Enter URL to scan: ").strip()
    scan_xss(url)

if __name__ == "__main__":
    main()