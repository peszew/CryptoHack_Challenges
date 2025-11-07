#!/usr/bin/env python3
from Crypto.Util.number import inverse, long_to_bytes
import math
import sys

# Dane (z Twojego output.txt / source.py)
N = 0x7fe8cafec59886e9318830f33747cafd200588406e7c42741859e15994ab62410438991ab5d9fc94f386219e3c27d6ffc73754f791e7b2c565611f8fe5054dd132b8c4f3eadcf1180cd8f2a3cc756b06996f2d5b67c390adcba9d444697b13d12b2badfc3c7d5459df16a047ca25f4d18570cd6fa727aed46394576cfdb56b41
e = 0x10001
c = 0x5233da71cc1dc1c5f21039f51eb51c80657e1af217d563aa25a8104a4e84a42379040ecdfdd5afa191156ccb40b6f188f4ad96c58922428c4c0bc17fd5384456853e139afde40c3f95988879629297f48d0efa6b335716a4c24bfee36f714d34a4e810a9689e93a0af8502528844ae578100b0188a2790518c695c095c9d677b

DATA_hex = "372f0e88f6f7189da7c06ed49e87e0664b988ecbee583586dfd1c6af99bf20345ae7442012c6807b3493d8936f5b48e553f614754deb3da6230fa1e16a8d5953a94c886699fc2bf409556264d5dced76a1780a90fd22f3701fdbcb183ddab4046affdc4dc6379090f79f4cd50673b24d0b08458cdbe509d60a4ad88a7b4e2921"
m_data = int(DATA_hex, 16)

def find_factor_via_pow_chain(m, N, max_k=16):
    a = m
    for k in range(1, max_k+1):
        a = pow(a, 2, N)
        g = math.gcd(a - 1, N)
        if 1 < g < N:
            return g, k
    return None, None

def main():
    p, k = find_factor_via_pow_chain(m_data, N, max_k=16)
    if p is None:
        print("Nie znaleziono czynnika metodą (gcd(m^(2^k)-1, N)).", file=sys.stderr)
        sys.exit(1)

    q = N // p
    print(f"Factor found at k={k}")
    print(f"p = {hex(p)}")
    print(f"q = {hex(q)}")


    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)

    # decrypt
    m_flag = pow(c, d, N)
    flag_bytes = long_to_bytes(m_flag)
    try:
        flag_text = flag_bytes.decode()
    except Exception:
        # nie-tekstowe bajty, pokaż surowe
        flag_text = None

    if flag_text:
        print(f"flag: {flag_text}")
    else:
        print("Odszyfrowano, ale wynik nie jest poprawnym UTF-8. Surowe bajty:")
        print(flag_bytes)

    # zapisz do pliku
    try:
        with open("flag.txt", "wb") as f:
            f.write(flag_bytes)
        print("Zapisano flagę do file: flag.txt")
    except Exception as exc:
        print(f"Nie udało się zapisać pliku: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
