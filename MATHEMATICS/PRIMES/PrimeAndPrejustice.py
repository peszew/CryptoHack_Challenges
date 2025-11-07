#!/usr/bin/env python3
import json
import itertools
import math
import sys
from tqdm import tqdm
from pwn import remote
from Crypto.Util.number import inverse, GCD

HOST = "socket.cryptohack.org"
PORT = 13385

def generate_basis(n):
    """Sieve-like: zwraca listę podstawowych liczb pierwszych < n (zaczynając od 2)."""
    if n < 3:
        return [2][:max(0,n)]
    basis = [True] * n
    for i in range(3, int(n**0.5) + 1, 2):
        if basis[i]:
            step = 2 * i
            start = i * i
            basis[start::step] = [False] * (((n - 1) - start)//step + 1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]

def miller_rabin(n, b):
    """
    Miller-Rabin test deterministyczny wykorzystujący wszystkie
    "b" jako górną granicę generowanych baz pierwszych.
    Zwraca True jeżeli n przechodzi testy, False jeśli z pewnością złożone.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    basis = generate_basis(b)
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for a in basis:
        if a % n == 0:
            continue
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

def xgcd(a, b):
    """Extended GCD. Zwraca (g, x, y) takie że a*x + b*y = g = gcd(a,b)."""
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t

def crt1(residues, modulos):
    """
    Prosty CRT dla listy (residues[i] mod modulos[i]).
    Zwraca (res, mod) lub (-1, -1) jeśli niespójne.
    """
    if not residues:
        return 0, 1
    cur_res, cur_mod = residues[0], modulos[0]
    for r, m in zip(residues[1:], modulos[1:]):
        g = GCD(cur_mod, m)
        if (r - cur_res) % g != 0:
            return -1, -1
        # Rozwiąż (cur_res + cur_mod * t) ≡ r (mod m)
        # Uproszczenie z rozszerzonym NWD
        # xgcd(a, b) zwraca (g, x, y) dla a*x + b*y = g
        gcd_val, s, tcoef = xgcd(m // g, cur_mod // g)
        # s,tcoef są współczynnikami; używamy ich aby znaleźć t
        cur_res = (cur_res * (m // g) * s + r * (cur_mod // g) * tcoef) % (cur_mod * (m // g))
        cur_mod = cur_mod * (m // g)
    return cur_res % cur_mod, cur_mod

def legendre_symbol(a, p):
    """Symbol Legendre'a (a|p) zwrócony jako 1 lub p-1 (-1 mod p)."""
    return pow(a, (p - 1)//2, p)

def build_fool_list(primes):
    fool = []
    for prime in primes:
        f = set()
        # iterujemy po prostych do 200*p aby sprawdzić warunki (zgodnie z oryginałem)
        for i in generate_basis(200 * prime)[1:]:
            if legendre_symbol(prime, i) == i - 1:
                f.add(i % (4 * prime))
        fool.append(sorted(f))
    return fool

def main_generation_and_attack():
    primes = generate_basis(64)
    print(f"Primes used (count): {len(primes)}")
    print(primes)

    fool = build_fool_list(primes)

    ks = [1, 998244353, 233]
    h = len(ks)

    # intersectujemy z warunkami dla kolejnych ks
    fool2 = []
    for idx, f in enumerate(fool):
        prime = primes[idx]
        m = prime * 4
        cur_set = set(f)
        for i in range(1, h):
            new_set = set()
            ksi = ks[i]
            try:
                inv_ksi = inverse(ksi, m)
            except Exception:
                inv_ksi = None
            if inv_ksi is None:
                cur_set = set()
                break
            for ff in f:
                val = ((ff + ksi - 1) * inv_ksi) % m
                if val % 4 == 3:
                    new_set.add(val)
            cur_set = cur_set.intersection(new_set)
        fool2.append(sorted(cur_set))

    # estymowane liczby kombinacji
    mm = 1
    for a in fool2:
        mm *= max(1, len(a))
    print("kombinacji (przybliżenie):", mm)
    print("fool2 sample lengths:", [len(x) for x in fool2])

    # upewnij się, że nie iterujemy po pustych listach
    if any(len(x) == 0 for x in fool2):
        print("Jedna z list restrykcji jest pusta -> brak rozwiązań CRT. Kończę.")
        return

    found = False
    fin = None
    facs = None

    for tup in itertools.product(*fool2):
        residues = list(tup)
        modulos = [primes[i] * 4 for i in range(len(tup))]

        # Dodajemy warunki dla ks[1] i ks[2] (tak jak w oryginale)
        residues.append(ks[1] - inverse(ks[2], ks[1]))
        modulos.append(ks[1])
        residues.append(ks[2] - inverse(ks[1], ks[2]))
        modulos.append(ks[2])

        sol, modul = crt1(residues, modulos)
        if sol == -1:
            continue

        # startujemy od offsetu tak jak w oryginale
        cur_t = (2**73) * modul + sol
        # przeszukujemy pewien zakres przyrostów
        for _ in tqdm(range(100000), desc="searching candidates"):
            # sprawdź czy cur_t jest pierwsze (użyjemy miller_rabin)
            if miller_rabin(cur_t, 64):
                candidate = cur_t
                candidate_facs = [candidate]
                fin_val = candidate
                # generujemy facs = ks[ii]*(candidate-1)+1 dla ii>=1
                valid = True
                for ii in range(1, h):
                    fval = ks[ii] * (candidate - 1) + 1
                    candidate_facs.append(fval)
                    fin_val *= fval
                # sprawdź złożoną liczbę fin_val
                if miller_rabin(fin_val, 64):
                    print("POTENCJALNY fin (passed MR):", fin_val.bit_length(), "bits")
                    print("fin:", fin_val)
                    print("factors:", candidate_facs)
                    if 600 <= fin_val.bit_length() <= 900:
                        found = True
                        fin = fin_val
                        facs = candidate_facs
                        break
            cur_t += modul
        if found:
            break

    if found:
        print("Generated pseudoprime with bit length:", fin.bit_length())
        print("Factors:", facs)
        solve(fin, facs)
    else:
        print("Failed to generate suitable pseudoprime")

def solve(p, facs):
    """
    Po wygenerowaniu silnego pseudoprima p i listy facs wyślij payload do serwera
    próbując ustawić 'a' tak, aby gcd(a, p) > 1 lub pow(a, p-1, p) != 1.
    """
    # p = product of facs? W oryginale p był "fin" (cała złożona liczba).
    # Zrobimy p jako fin (tu nazwa parametru jest zgodna z main call).
    for i, fac in enumerate(facs):
        print(f"\nTrying with factor {i}: {fac}")
        for k in range(2, 10):
            a = k * fac
            if a >= p:
                break
            result_loc = pow(a, p-1, p)
            print(f"Trying a = {k} * factor = {a} -> pow(a, p-1, p) = {result_loc}")

            r = remote(HOST, PORT)
            r.recvuntil(b"primes!\n")

            payload = json.dumps({"base": a, "prime": p})
            r.sendline(payload.encode())

            response = r.recvline().decode(errors="ignore").strip()
            try:
                data = json.loads(response)
                if "Response" in data:
                    print("Server response:", data["Response"])
                    if "crypto{" in data["Response"]:
                        print("\n*** FOUND FLAG! ***")
                        r.close()
                        return
                else:
                    print("Raw JSON:", data)
            except json.JSONDecodeError:
                print("Raw response:", response)
            r.close()

if __name__ == "__main__":
    main_generation_and_attack()
