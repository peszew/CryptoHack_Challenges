from random import randrange
import requests

NDATA = 120  # amount of data to use
NKS = 32     # number of keystream bytes to use
FLAGLEN = 34
NONCELEN = 256 - FLAGLEN


# Given a long partial RC4 key, produce nks bytes that approximate keystream
def PC4(pkey, nks):
    
    # We can do most of the run-up
    S = [ i for i in range(256) ]
    j = 0
    for i in range(len(pkey)):
        j = (j + S[i] + pkey[i]) & 0xff
        S[i], S[j] = S[j], S[i]
    for i in range(len(pkey), 256):
        S[i] = -1 

    # Generate as much approximated keystream as it is possible
    ks = []
    j = 0
    for i in range(1, nks+1):
        if S[i] < 0: 
            break
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]
        if S[j] < 0: # cant compute without
            ks.append(-1)
        else:
            sij = (S[i] + S[j]) & 0xff
            if S[sij] < 0: # without this can't compute key
                ks.append(-1)
            else:
                ks.append(S[sij])
    return ks

    
# Get some RC4 key using long random nonces
nonces = []
ks = []
print("Getting data...")
for _ in range(NDATA):
    randnonce = bytes([randrange(256) for _ in range(NONCELEN)])
    nonces.append(list(randnonce))
    resp =requests.get(f"http://aes.cryptohack.org/oh_snap/send_cmd/"+"00"*NKS+"/"+randnonce.hex()+"/").json()
    ks.append(list(bytes.fromhex(resp['error'][17:])))


# Attack to recover flag
print("Recovering flag:")
flag = list(b'crypto{')
while len(flag) < FLAGLEN:
    highscore = -1
    # Guess the next flag byte:
    for guess in range(32, 128):
        score = 0
        for i in range(NDATA):
            output = PC4(nonces[i] + flag + [guess], NKS)
            score += sum([ v[0]==v[1] for v in zip(output, ks[i])])
        if score > highscore:
            highscore = score
            best = guess
    flag.append(best)
    print("".join([chr(x) for x in flag]))
    NDATA -= 2 