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
