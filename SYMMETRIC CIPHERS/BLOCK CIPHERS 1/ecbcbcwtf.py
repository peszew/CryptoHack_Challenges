import requests
from Crypto.Util.number import long_to_bytes

BASE = "https://aes.cryptohack.org/ecbcbcwtf"

# 1. Pobierz ciphertext flagi
resp = requests.get(f"{BASE}/encrypt_flag/").json()
ciphertext_hex = resp["ciphertext"]
ciphertext = bytes.fromhex(ciphertext_hex)

# 2. Poproś serwer o ECB decrypt
resp2 = requests.get(f"{BASE}/decrypt/{ciphertext_hex}/").json()
dec_hex = resp2["plaintext"]
decrypted = bytes.fromhex(dec_hex)

# Podziel na bloki po 16 bajtów
blocks_ct = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
blocks_dec = [decrypted[i:i+16] for i in range(0, len(decrypted), 16)]

# 3. Odszyfruj CBC lokalnie
plaintext = b""

for i in range(1, len(blocks_ct)):   # zaczynamy od bloku 1 (C1)
    P = bytes([blocks_dec[i][j] ^ blocks_ct[i-1][j] for j in range(16)])
    plaintext += P

print("\n[+] CBC-PLAIN:", plaintext)
print("[+] FLAG:", plaintext.decode(errors="ignore"))
