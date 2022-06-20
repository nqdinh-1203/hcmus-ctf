from fnmatch import translate
from random import shuffle

msg = 'DIGCQ-IZR{ODAONCO_NHPKQ_ZX_BNAS_IFSBZXUFAG}'
''' with open('../Secret/msg.txt') as file:
    msg = file.read().upper() '''

ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

SUB_ALPHABET = list(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

while not 'CTF' in msg:
    shuffle(SUB_ALPHABET)

    translate_dict = {}
    for u, v in zip(ALPHABET, SUB_ALPHABET):
        translate_dict[u] = v

    msg.translate(translate_dict)
    
print(msg)