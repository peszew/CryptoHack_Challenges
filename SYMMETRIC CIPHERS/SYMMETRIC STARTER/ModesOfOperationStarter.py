import requests
import binascii

BASE = "https://aes.cryptohack.org/block_cipher_starter"

# 1) Pobranie szyfrogramu flagi
resp1 = requests.get(f"{BASE}/encrypt_flag/").json()
ct_hex = resp1["ciphertext"]
print("[+] Ciphertext:", ct_hex)

# 2) szyfrogram -> deszyft
resp2 = requests.get(f"{BASE}/decrypt/{ct_hex}/").json()
pt_hex = resp2["plaintext"]
print("[+] Plaintext hex:", pt_hex)

# 3) hex → ASCII
flag = binascii.unhexlify(pt_hex).decode()
print("\nFLAG =", flag)
