# Basic modular arithmetic examples
p = 17
print("3^17 mod 17 =", pow(3, 17, p))
print("5^17 mod 17 =", pow(5, 17, p))
print("7^16 mod 17 =", pow(7, 16, p))

# Fermat's little theorem with a large prime modulus
p = 65537
a = 273246787654
print("a^65536 mod 65537 =", pow(a, 65536, p))
