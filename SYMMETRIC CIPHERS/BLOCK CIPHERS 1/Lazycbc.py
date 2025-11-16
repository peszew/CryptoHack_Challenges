import requests
BASE = "https://aes.cryptohack.org/lazy_cbc"  # change if needed
def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

# 1) request a 3-block ciphertext for known plaintext
plain = b"a" * 16 * 3
r = requests.get(f"{BASE}/encrypt/{plain.hex()}/")
r.raise_for_status()
cipher_hex = r.json()["ciphertext"]
print("ciphertext:", cipher_hex)

# 2) extract C0 and craft fake ciphertext: C0 || zero || C0
c0 = bytes.fromhex(cipher_hex[:32])
zero = b"\x00" * 16
fake = c0 + zero + c0
fake_hex = fake.hex()

# 3) send fake and parse decrypted hex from the error
r2 = requests.get(f"{BASE}/receive/{fake_hex}/")
data = r2.json()
if "error" not in data:
    raise SystemExit("unexpected response, no error field")
err = data["error"]
prefix = "Invalid plaintext: "
if prefix not in err:
    raise SystemExit("unexpected error format: " + err)
decrypted_hex = err.split(prefix)[1]
print("decrypted hex:", decrypted_hex)

# 4) split and xor P0 ^ P2 to recover key/iv
dec = bytes.fromhex(decrypted_hex)
p0 = dec[:16]
p2 = dec[32:48]
key = xor_bytes(p0, p2)
print("recovered key (hex):", key.hex())

# 5) fetch flag using recovered key
r3 = requests.get(f"{BASE}/get_flag/{key.hex()}/")
r3.raise_for_status()
resp = r3.json()

if "plaintext" in resp:
    flag = bytes.fromhex(resp["plaintext"]).decode()
    print("FLAG:", flag)
else:
    print("get_flag response:", resp)