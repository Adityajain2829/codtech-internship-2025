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
