import socket

def scan_ports(target, ports=[21, 22, 23, 80, 443]):
    print(f"Scanning {target} for open ports...")
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"[+] Port {port} is open")
            else:
                print(f"[-] Port {port} is closed")

if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    scan_ports(target_ip)