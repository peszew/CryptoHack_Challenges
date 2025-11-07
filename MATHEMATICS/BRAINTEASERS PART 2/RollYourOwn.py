from pwn import *
import json

def solve():
    # Połącz z serwerem
    conn = remote('socket.cryptohack.org', 13403)

    try:
        # Odbierz linię z q
        conn.recvuntil(b'Prime generated: ')
        q_hex = conn.recvline().strip().decode().strip().strip('"')
        # dopuszczamy format z 0x lub bez
        if q_hex.startswith("0x") or q_hex.startswith("0X"):
            q = int(q_hex, 16)
        else:
            q = int(q_hex, 16)
        log.info(f"Received q (hex): {q_hex}")
        log.info(f"Parsed q (int): {q}")

        n = q * q
        g = q + 1

        # walidacja pow(g, q, n) == 1 przed wysłaniem
        if pow(g, q, n) != 1:
            log.warning("pow(g,q,n) != 1 dla g = q+1. Szukam małego g spełniającego warunek.")
            for small in range(2, 20):
                if pow(small, q, n) == 1:
                    g = small
                    log.info(f"Znaleziono alternatywne g = {g}")
                    break
            else:
                log.error("Nie udało się znaleźć g spełniającego warunek. Kończę.")
                conn.close()
                return

        log.info(f"Using n = q^2: {n}")
        log.info(f"Using g: {g} (hex: {hex(g)})")

        # odebranie promptu i wysłanie (g,n)
        conn.recvuntil(b'Send integers (g,n) such that pow(g,q,n) = 1: ')
        payload = json.dumps({"g": hex(g), "n": hex(n)})
        conn.sendline(payload.encode())
        log.info("Sent g and n")

        # Odbierz publiczny klucz h
        conn.recvuntil(b'Generated my public key: ')
        h_hex = conn.recvline().strip().decode().strip().strip('"')
        if h_hex.startswith("0x") or h_hex.startswith("0X"):
            h = int(h_hex, 16)
        else:
            h = int(h_hex, 16)
        log.info(f"Received h (hex): {h_hex}")
        log.info(f"Parsed h (int): {h}")

        # Rozwiązanie: (q+1)^x = 1 + x*q (mod q^2) => h = 1 + x*q (mod q^2)
        # więc x = (h - 1) // q
        if (h - 1) % q != 0:
            log.warning("h-1 nie jest podzielne przez q. Wynik może być nieprawidłowy.")
        x = (h - 1) // q
        log.info(f"Found x (int): {x}")

        # Wyślij x
        conn.recvuntil(b'What is my private key: ')
        payload = json.dumps({"x": hex(x)})
        conn.sendline(payload.encode())

        # Odbierz flagę / odpowiedź (do końca)
        response = conn.recvall(timeout=5)
        if response:
            try:
                text = response.decode(errors='ignore')
                log.success(f"Received response: {text}")
            except Exception:
                log.success(f"Received binary response: {response}")
        else:
            log.warning("Nie otrzymano dalszej odpowiedzi od serwera.")

    except EOFError:
        log.error("Połączenie zamknięte przez serwer. Parametry prawdopodobnie odrzucone.")
    except Exception as e:
        log.error(f"Wystąpił błąd: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    solve()
