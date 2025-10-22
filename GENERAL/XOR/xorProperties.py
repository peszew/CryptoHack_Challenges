# compute_flag.py
def bxor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

KEY1_hex = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
KEY2_xor_KEY1_hex = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
KEY2_xor_KEY3_hex = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
FLAG_xor_ALL_hex = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

k1 = bytes.fromhex(KEY1_hex)
k2_xor_k1 = bytes.fromhex(KEY2_xor_KEY1_hex)
k2_xor_k3 = bytes.fromhex(KEY2_xor_KEY3_hex)
flag_xor_all = bytes.fromhex(FLAG_xor_ALL_hex)

# recover keys
k2 = bxor(k2_xor_k1, k1)      # KEY2 = (KEY2 ^ KEY1) ^ KEY1
k3 = bxor(k2_xor_k3, k2)      # KEY3 = (KEY2 ^ KEY3) ^ KEY2

# recover flag
flag = bxor(flag_xor_all, bxor(bxor(k1, k2), k3))  # FLAG = (FLAG^K1^K3^K2) ^ K1 ^ K3 ^ K2

print("crypto{" + flag.decode() + "}")
