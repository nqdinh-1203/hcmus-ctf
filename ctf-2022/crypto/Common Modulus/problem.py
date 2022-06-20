import math
from Crypto.Util.number import getPrime, bytes_to_long

with open("flag.txt") as f:
    flag = bytes_to_long(f.readline().encode())

k = 8
n = getPrime(2048)*getPrime(2048)
print(f"n = {n}")

l = [getPrime(32) for i in range(k)]
print(f"l = {l}")

C = []
for i in range(k):
    li = l[:i] + l[i+1:]
    e = math.prod(li)
    C.append(pow(flag, e, n))

print(f"C = {C}")