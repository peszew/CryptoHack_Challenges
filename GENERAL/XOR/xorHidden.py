ct = bytes.fromhex("73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d")
for k in range(256):
    pt = bytes(b ^ k for b in ct)
    try:
        s = pt.decode('ascii')
    except:
        continue
    if all(32 <= ord(c) <= 126 for c in s):
        print(k, s)
