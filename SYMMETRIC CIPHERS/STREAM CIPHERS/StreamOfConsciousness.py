import requests
import json
encryptions=[]
for i in range(100):  #big enough number to ensure you have all the ciphertexts
	site="https://aes.cryptohack.org/stream_consciousness/encrypt/"
	r=requests.get(site)
	t=json.loads(r.text)
	ct=t['ciphertext']
	encryptions.append(ct)
	print(i)

encryptions=list(set(encryptions))  #removing all duplicates, results in a list of 22 encryptions
encryptions=sorted(encryptions,key= lambda x:len(x)) #sorted by length
encryptions=[bytes.fromhex(i) for i in encryptions]
originalList=encryptions

def bytewiseXor(m1,m2):   #taking xor of two messages till the length of smaller message
	xorlen=min(len(m1),len(m2))
	return bytes([m1[i]^m2[i] for i in range(xorlen)])

def printDecryptions(j,crib):   #function to print the decryptions using the crib and j is the ciphertext number for which we guessed the crib is for
	for i in range(len(encryptions)):
		print(decryptions[i]+bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[j])))

crib=b'crypto{'
for i in range(len(encryptions)):
	if all([ bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[j])).decode().isprintable()  for j in range(len(encryptions))] ):
		textNo=i
 
 #textNo=4 so we can se flag is ciphertext 4 lets try printing decryptions
decryptions=[b'' for i in range(len(encryptions))]
decryptions[textNo]+=crib
for i in range(len(encryptions)):
	if i!=textNo:
		decryptions[i]+=bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[textNo]))

encryptions=[i[len(crib):] for i in encryptions] # truncating encryptions by length of crib


for i in decryptions:
  print(i)

crib=b'appy'
textNo=17
printDecryptions(textNo,crib)

decryptions[textNo]+=crib
for i in range(len(encryptions)):
	if i!=textNo:
		decryptions[i]+=bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[textNo]))

encryptions=[i[len(crib):] for i in encryptions]


textNo=18
crib=b'bly'
printDecryptions(textNo,crib)

decryptions[textNo]+=crib
for i in range(len(encryptions)):
	if i!=textNo:
		decryptions[i]+=bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[textNo]))

encryptions=[i[len(crib):] for i in encryptions]

#What a nasty smell  so lets try out "mell " as the crib and text no is 5
textNo=5
crib=b'mell '
printDecryptions(textNo,crib)

decryptions[textNo]+=crib
for i in range(len(encryptions)):
	if i!=textNo:
		decryptions[i]+=bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[textNo]))

encryptions=[i[len(crib):] for i in encryptions]
textNo=7
crib=b'hing '
printDecryptions(textNo,crib)

decryptions[textNo]+=crib
for i in range(len(encryptions)):
	if i!=textNo:
		decryptions[i]+=bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[textNo]))

encryptions=[i[len(crib):] for i in encryptions]
crib=b'thing '
textNo=13
printDecryptions(textNo,crib)

decryptions[textNo]+=crib
for i in range(len(encryptions)):
	if i!=textNo:
		decryptions[i]+=bytewiseXor(crib,bytewiseXor(encryptions[i],encryptions[textNo]))

encryptions=[i[len(crib):] for i in encryptions]
textNo=19
crib=b'ing '
printDecryptions(textNo,crib)
