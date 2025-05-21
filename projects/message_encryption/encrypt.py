# Purpose: Encrypt a message and generate a password to decrypt later

# DISCLAIMER:
# This script is for educational purposes only and is not intended for use in production environments.
# It demonstrates basic encryption concepts using AES-CBC and PBKDF2.
# For secure applications, consider using authenticated encryption modes (e.g., AES-GCM) and secure key storage practices.

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

# Your private journal entry and password
journal_entry = input("Enter your message: ")  # Replace with your journal content
password = input("Create a password: ")  # Replace with your secure password

# Encode the data
secret_data = journal_entry.encode('utf-8')
password_bytes = password.encode('utf-8')

# Generate a salt and IV
salt = os.urandom(16)
iv = os.urandom(16)

# Derive a key from the password
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
encryption_key = kdf.derive(password_bytes)

# Apply PKCS7 padding
padder = padding.PKCS7(128).padder()
padded_data = padder.update(secret_data) + padder.finalize()

# Encrypt the data
cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

# Combine and encode to Base64
combined = salt + iv + encrypted_data
encrypted_base64 = base64.b64encode(combined).decode()

# Output the encrypted result
print("\n--- COPY THIS ENCRYPTED TEXT ---")
print(encrypted_base64)
print("\n--- USE THIS PASSWORD TO DECRYPT LATER ---")
print(password)
