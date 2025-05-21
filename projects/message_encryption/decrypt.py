# Purpose: decrypt your message using your password

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Paste the encrypted Base64 string and the password you used
encrypted_base64 = input("paste_encrypted_text_here: ")  # <-- Replace with your encrypted text
password = input("your_strong_password_here: ")          # <-- Replace with your password

# Decode and split components
data = base64.b64decode(encrypted_base64)
salt, iv, ciphertext = data[:16], data[16:32], data[32:]

# Derive the key from the password
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password.encode('utf-8'))

# Decrypt
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Remove padding
unpadder = padding.PKCS7(128).unpadder()
plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

# Output the original journal entry
print("\n--- DECRYPTED MESSAGE ---")
print(plaintext.decode('utf-8'))
