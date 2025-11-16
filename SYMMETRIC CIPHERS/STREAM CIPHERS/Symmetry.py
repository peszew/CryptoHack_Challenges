from pwn import*
import requests

def encrypt(plain, iv):
    url = "https://aes.cryptohack.org/symmetry/encrypt"
    url += "/"
    url += plain
    url += "/"
    url += iv
    r = requests.get(url).json()
    return bytes.fromhex(r["ciphertext"])

def encrypt_flag():
    url = "https://aes.cryptohack.org/symmetry/encrypt_flag"
    r = requests.get(url).json()
    return bytes.fromhex(r["ciphertext"])

iv_ciphertext = encrypt_flag()
iv = iv_ciphertext[:16].hex()
ciphertext = iv_ciphertext[16:]


ciphertext_chosen = encrypt("00"*33, iv)
print(xor(ciphertext,ciphertext_chosen).decode())
