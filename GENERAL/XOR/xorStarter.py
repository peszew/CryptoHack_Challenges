from pwn import xor

label = b"label"   # bytes required
new = xor(label, 13)            # returns bytes
flag = b"crypto{" + new + b"}"
print(flag.decode())            # display as string
