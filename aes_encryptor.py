
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import tkinter as tk
from tkinter import filedialog, messagebox

def encrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = filename + ".enc"
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = filename[:-4]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def browse_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def encrypt_file():
    file_path = file_entry.get()
    password = pass_entry.get()
    if file_path and password:
        encrypt(getKey(password), file_path)
        messagebox.showinfo("Success", "File encrypted successfully!")
    else:
        messagebox.showwarning("Missing Info", "Please provide a file and password.")

def decrypt_file():
    file_path = file_entry.get()
    password = pass_entry.get()
    if file_path and password:
        decrypt(getKey(password), file_path)
        messagebox.showinfo("Success", "File decrypted successfully!")
    else:
        messagebox.showwarning("Missing Info", "Please provide a file and password.")

# GUI
root = tk.Tk()
root.title("AES-256 File Encryptor")

tk.Label(root, text="File:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=10)
pass_entry = tk.Entry(root, show='*', width=40)
pass_entry.grid(row=1, column=1, padx=10)

tk.Button(root, text="Encrypt", command=encrypt_file).grid(row=2, column=0, pady=20)
tk.Button(root, text="Decrypt", command=decrypt_file).grid(row=2, column=1, pady=20)

root.mainloop()
