from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image
import io
import os

# Convert image to bytes
def image_to_bytes(image_path):
    with open(image_path, 'rb') as img_file:
        return img_file.read()

# Convert bytes back to image
def bytes_to_image(img_bytes, output_path):
    img = Image.open(io.BytesIO(img_bytes))
    img.save(output_path)

# Encrypt image using AES
def encrypt_image(image_path, key):
    iv = get_random_bytes(16)
    img_bytes = image_to_bytes(image_path)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(img_bytes, AES.block_size))
    return iv + encrypted_bytes  # Prepend IV

# Decrypt image using AES
def decrypt_image(encrypted_bytes, key):
    iv = encrypted_bytes[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes[AES.block_size:]), AES.block_size)
    return decrypted_bytes

def main():
    # --- CONFIGURATION ---
    key = get_random_bytes(16)  # Use os.urandom(16) for secure persistence
    original_image = 'input_image.jpg'
    encrypted_file = 'encrypted_image.enc'
    decrypted_image = 'decrypted_image.jpg'

    # --- ENCRYPT ---
    encrypted_data = encrypt_image(original_image, key)
    with open(encrypted_file, 'wb') as f:
        f.write(encrypted_data)
    print(f"[✔] Image encrypted and saved as '{encrypted_file}'")

    # --- DECRYPT ---
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_image(encrypted_data, key)
    bytes_to_image(decrypted_data, decrypted_image)
    print(f"[✔] Image decrypted and saved as '{decrypted_image}'")

if __name__ == '__main__':
    main()
