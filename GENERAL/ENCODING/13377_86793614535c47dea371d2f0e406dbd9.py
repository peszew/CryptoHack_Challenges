#!/usr/bin/env python3
from pwn import remote
import json, base64, codecs

def json_recv(r):
    return json.loads(r.recvline().decode())

def json_send(r, h):
    r.sendline(json.dumps(h).encode())

def decode_msg(obj):
    t = obj["type"]
    v = obj["encoded"]
    if t == "base64":
        return base64.b64decode(v).decode()
    if t == "hex":
        return bytes.fromhex(v).decode()
    if t == "rot13":
        return codecs.decode(v, "rot_13")
    if t == "bigint":
        # v is like "0x..."
        n = int(v, 0)
        length = (n.bit_length() + 7) // 8 or 1
        return n.to_bytes(length, "big").decode()
    if t == "utf-8":
        # v is a list of integers
        return "".join(chr(i) for i in v)
    raise ValueError("unknown type "+t)

r = remote("socket.cryptohack.org", 13377)
try:
    # initial receive
    msg = json_recv(r)
    while True:
        print("TYPE:", msg.get("type"))
        decoded = decode_msg(msg)
        json_send(r, {"decoded": decoded})
        msg = json_recv(r)
        if "flag" in msg:
            print("FLAG:", msg["flag"])
            break
except Exception as e:
    print("error:", e)
finally:
    r.close()
