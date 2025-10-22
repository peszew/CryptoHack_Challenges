def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

p = 26513
q = 32321

g, u, v = extended_gcd(p, q)
print("gcd:", g)
print("u:", u)
print("v:", v)
