import binascii

def xor_hex(hex1, hex2):

    b1 = binascii.unhexlify(hex1)
    b2 = binascii.unhexlify(hex2)
    
    result_bytes = bytes([_a ^ _b for _a, _b in zip(b1, b2)])
    
    return binascii.hexlify(result_bytes).decode()

def solve():
   
    ciphertext_hex = "0e0b213f26041e480b26217f27342e175d0e070a3c5b183e2526217f27342e175d0e077e263451150104"
    
    known_plaintext = "crypto{"
    
    known_plaintext_hex = known_plaintext.encode().hex()
    
    ciphertext_part_hex = ciphertext_hex[:len(known_plaintext_hex)]
    
    print(f"Known Plaintext: {known_plaintext}")
    print(f"Plaintext Hex:   {known_plaintext_hex}")
    print(f"Ciphertext Hex:  {ciphertext_part_hex}")
    print("-" * 30)

    key_part_hex = xor_hex(known_plaintext_hex, ciphertext_part_hex)
    key_part_ascii = binascii.unhexlify(key_part_hex).decode()
    
    print(f"Derived Key Part (Hex):   {key_part_hex}")
    print(f"Derived Key Part (ASCII): {key_part_ascii}")
    print("-" * 30)
    
    key = "myXORkey"
    key_bytes = key.encode()
    key_len = len(key_bytes)
    
    print(f"Guessed Full Key: {key}\n")
    
    ciphertext_bytes = binascii.unhexlify(ciphertext_hex)
    plaintext_bytes = bytearray()
    
 
    for i in range(len(ciphertext_bytes)):
        key_byte = key_bytes[i % key_len]
        plain_byte = ciphertext_bytes[i] ^ key_byte
        plaintext_bytes.append(plain_byte)
 
    try:
        flag = plaintext_bytes.decode('ascii')
        print(f"Decrypted Flag: {flag}")
    except UnicodeDecodeError:
        print(f"Decrypted Bytes (contains non-ASCII): {plaintext_bytes}")

if __name__ == "__main__":
    solve()