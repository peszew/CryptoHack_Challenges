import requests
import hashlib
from Crypto.Cipher import AES

# 1) Pobieranie ciphertext 
BASE = "https://aes.cryptohack.org/passwords_as_keys"
ciphertext = requests.get(f"{BASE}/encrypt_flag/").json()["ciphertext"]
cipher_bytes = bytes.fromhex(ciphertext)

# 2) Pobieranie wordlisty
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
words = requests.get(WORDLIST_URL).text.split()

print("[+] Loaded words:", len(words))

# 3) Lokalny brute force AES-ECB
for w in words:
    key = hashlib.md5(w.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        pt = cipher.decrypt(cipher_bytes)
        text = pt.decode("utf-8", errors="ignore")
    except:
        continue

    if text.startswith("crypto{"):
        print("\n[+] FOUND!")
        print("Password word:", w)
        print("FLAG:", text)
        break
