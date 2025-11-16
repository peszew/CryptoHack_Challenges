import requests, io
from PIL import Image
import numpy as np
from pwn import xor
from Crypto.Util.number import long_to_bytes, bytes_to_long

URL = "http://aes.cryptohack.org/bean_counter/encrypt"
# every PNG image begins with the following 16 plaintext bytes.
PNG_PREFIX = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'

r = requests.get(url=URL)
enc_bytes = bytes.fromhex(r.json()['encrypted'])

# Plaintext = Keystream XOR Ciphertext --> Keystream = Plaintext XOR Ciphertext
keystream = xor(PNG_PREFIX, enc_bytes[:16])

# Decrypt the ciphertext using the keystream above
pt = xor(enc_bytes, keystream)

image = Image.open(io.BytesIO(pt))
# Reproduce the image with the plaintext bytes
image.save('bean_flag.png')