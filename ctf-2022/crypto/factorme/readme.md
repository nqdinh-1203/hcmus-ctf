## HCMUS-CTF 2022: Challenge name

![warmup category](https://img.shields.io/badge/Category-Cryptography-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-Naul-blue.svg)  
![solves](https://img.shields.io/badge/Solves-16-lightgrey.svg)

### Description
- Forgot

### Hints
- None

### Attached files
- Lost

### Summary
- given $e,d$ such that $ed \equiv 1 \mod \varphi(N)$, we can easy factor $N$
- for more detail about this factor, you can visit [here](https://crypto.stackexchange.com/questions/6361/is-sharing-the-modulus-for-multiple-rsa-key-pairs-secure/14713)
- after obtain $p$, the first factor of $N$, we can cumpute the number factor of $N$ by $\left\lceil \frac{bits(N)}{bits(p)} \right\rceil$

### Detailed solution
python implement
```python
import pwn
import time
import random
from math import gcd, ceil
from gmpy2 import is_prime
from Crypto.Util.number import getPrime


def remove_even(n):
    if n == 0:
        return (0, 0)
    r = n
    t = 0
    while (r & 1) == 0:
        t = t + 1
        r = r >> 1
    return (r, t)


def get_root_one(x, k, N):
    (r, t) = remove_even(k)
    oldi = None
    i = pow(x, r, N)
    while i != 1:
        oldi = i
        i = (i*i) % N
    if oldi == N-1:
        return None
    return oldi


def factor_prime(N, phi):
    while True:
        while True:
            e = getPrime(16)
            if gcd(e, phi) == 1:
                d = pow(e, -1, phi)
                break

        k = e*d - 1
        y = None
        while not y:
            x = random.randrange(2, N)
            y = get_root_one(x, k, N)

        p = gcd(y-1, N)
        if is_prime(p):
            return p
        q = gcd(y+1, N)
        if is_prime(q):
            return q


def factor_count(N, phi):
    return ceil(N.bit_length()/factor_prime(N, phi).bit_length())


s = pwn.remote('103.245.250.31', 30521)
start_time = time.time()

for i in range(60):
    s.recvline()
    N = int(s.recvline().decode().split(':')[-1])
    phi = int(s.recvline().decode().split(':')[-1])
    print("Round", i)

    n_fac = factor_count(N, phi)
    s.sendline(str(n_fac).encode())

end_time = time.time()
print("Time taken:", end_time - start_time, "seconds")
print(s.recvline())
```

### Flag
```
HCMUS-CTF{H0p3_y0u_didn7_f4ct0r1s3_th353_Ns}
```