from sympy import isprime

aList = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]

def findX(p):
    for x in range(1, p):  # x < p
        valid = True
        for i in range(len(aList) - 1):
            if (aList[i] * x) % p != aList[i + 1]:
                valid = False
                break
        if valid:
            return x
    return None

for p in range(101, 1000):
    if isprime(p):
        x = findX(p)
        if x is not None:
            print("crypto{" + str(p) + "," + str(x) + "}")
            break
