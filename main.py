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
