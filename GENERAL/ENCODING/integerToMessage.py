from Crypto.Util.number import long_to_bytes

integer = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

# Convert the integer into a sequence of bytes
message_bytes = long_to_bytes(integer)

# Decode the bytes into a human-readable string
message = message_bytes.decode('utf-8')

print(f"The decoded message is: {message}")