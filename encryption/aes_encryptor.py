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
