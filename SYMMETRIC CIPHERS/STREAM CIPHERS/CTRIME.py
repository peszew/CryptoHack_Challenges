from Crypto.Cipher import AES
from Crypto.Util import Counter
import zlib
import requests

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_{}0123456789abcdefghijklmnopqrstuvwxyz"

def encrypt(plaintext):
    url = 'https://aes.cryptohack.org/ctrime/encrypt/'
    url = url + plaintext.hex()
    url = url + '/'
    r = requests.get(url)
    js = r.json()
    output = js['ciphertext']
    return output

flag = b"crypto{"
last_chr = b""
while last_chr != b"}":
    send = flag + b"*"
    out = encrypt(send*2)
    for c in alpha:
        print(c)
        send = flag + c.encode()
        out2 = encrypt(send*2)
        print(len(out),len(out2))
        if len(out2) < len(out):
            flag += c.encode()
            last_chr = c.encode()
            break
    print(flag)
