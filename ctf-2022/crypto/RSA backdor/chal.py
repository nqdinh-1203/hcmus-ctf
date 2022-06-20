from Crypto.Util.number import *

# with open("../flag.txt") as file:
#     FLAG = file.read().encode()
FLAG = b'123'

p, q = -1, -1
n = -1
e = 65537

while True:
    p = getPrime(512)
    q = int(str(p), 13)
    if isPrime(q):
        n = p * q
        print('p: ', p)
        print('Public key n = ', n)
        break

print(f'ct = ', pow(bytes_to_long(FLAG), e, n))
