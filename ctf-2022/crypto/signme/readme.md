## HCMUS-CTF 2022: Challenge name

![warmup category](https://img.shields.io/badge/Category-Cryptography-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-500-blue.svg)  
![author](https://img.shields.io/badge/Author-naul-blue.svg)
![solves](https://img.shields.io/badge/Solves-16-lightgrey.svg)

### Description
- Forgot

### Hints
- None

### Attached files
- [chal.py](chal.py)

### Summary
- The challange use Elgamal signature schema
- To create a valid signature, we need to recover $x$
- The challange give us $g, p, r, s$ and we can recover $h$ using the same code as challange
- If we sign the message `b'\x00'` then we get $k \gets 1$
- Now, from the fomular $s \equiv (h - xr)k^{-1} \mod {p-1}$, we can recover $x$
- After obtain $x$, we can create a valid signature using Elgamal signature schema

### Detailed solution
Python implement:
```python
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from base64 import b64encode
from hashlib import sha256


def remove_even(n):
    if n == 0:
        return (0, 0)
    r = n
    t = 0
    while (r & 1) == 0:
        t = t + 1
        r = r >> 1
    return (r, t)


def recover_x(h, r, p):
    _r, _t = remove_even(r)

    x = (h-s*k) % (p-1)*pow(_r, -1, p-1) % (p-1)
    for _ in range(_t):
        x = x//2 if x//2 % 2 == 0 else (x + (p-1))//2 % (p-1)

    return x


def forgery_signnature(x, g, p, pt):
    k = 1  # any number coprime with p-1
    r = pow(g, k, p)
    h = bytes_to_long(sha256(pt).digest())
    s = ((h - x * r) * inverse(k, p - 1)) % (p - 1)

    return (r, s)


# define some special values
pt = b'AA=='
h = bytes_to_long(sha256(pt).digest())
k = 1


# gather informaion
print("Please access the challange and get the public key")
g = int(input("g = "))
p = int(input("p = "))
print(f"Please sign the message: {pt.decode()}")
r = int(input("r = "))
s = int(input("s = "))


# recover x
x = recover_x(h, r, p)
print('Secret x =', x)


# create signature
pt = input("Message needs to be signed: ").encode()
r, s = forgery_signnature(x, g, p, pt)


# make sure the signature is valid
h = bytes_to_long(sha256(pt).digest())
y = pow(g, x, p)
assert pow(g, h, p) == (pow(y, r, p) * pow(r, s, p)) % p


# print out results
print("Here is your signature:")
print(f"r = {b64encode(long_to_bytes(r)).decode()}")
print(f"s = {b64encode(long_to_bytes(s)).decode()}")
```
Example:
```
└─$ python ./test.py
Please access the challange and get the public key
g = 70209754836850153197827245357246067773153880026518673775549936828609655663624
p = 99489312791417850853874793689472588065916188862194414825310101275999789178243
Please sign the message AA==
r = 70209754836850153197827245357246067773153880026518673775549936828609655663624
s = 18905745849522780693834385547943046983559348486129312260711276083947558901759
Secret x = 80318713694735405124095954672334003718416016814076751678195503189989638841502
Message needs to be signed: VMEjmnhU4EZfGFN3roRjpZIiFkgNufJjmoBqkD970W0=
Here is your signature:
r = mzlQIMp/UWeijN1zcwYCYlGI0bAAWOzSjnQrH07G7Ag=
s = SZnfjVOaGZxz2Whxt4kY9F97nrY33Ccp8XO6ZfAQF2Q=
```
```
└─$ nc 103.245.250.31 31850
Welcome to our sign server
You have only 32 attempts left
0. Get public key
1. Sign a message
2. Verify a message
3. Get flag
Select an option: 0
g = 70209754836850153197827245357246067773153880026518673775549936828609655663624
p = 99489312791417850853874793689472588065916188862194414825310101275999789178243
You have only 32 attempts left
0. Get public key
1. Sign a message
2. Verify a message
3. Get flag
Select an option: 1
Input message you want to sign: AA==
Signature (r, s):  (70209754836850153197827245357246067773153880026518673775549936828609655663624, 18905745849522780693834385547943046983559348486129312260711276083947558901759)
You have only 31 attempts left
0. Get public key
1. Sign a message
2. Verify a message
3. Get flag
Select an option: 3
Could you sign this for me:  VMEjmnhU4EZfGFN3roRjpZIiFkgNufJjmoBqkD970W0=
Input r: mzlQIMp/UWeijN1zcwYCYlGI0bAAWOzSjnQrH07G7Ag=
Input s: SZnfjVOaGZxz2Whxt4kY9F97nrY33Ccp8XO6ZfAQF2Q=
Congratulation, this is your flag:  HCMUS-CTF{B4se64_15_1nt3r3stin9}
```

### Flag
```
HCMUS-CTF{B4se64_15_1nt3r3stin9}
```