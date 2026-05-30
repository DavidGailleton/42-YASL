from string import ascii_lowercase, ascii_uppercase, digits
from sys import argv
from math import sqrt

if len(argv) != 1:
    exit
base_64 = ascii_uppercase + ascii_lowercase + digits + "+/"
print(base_64)
with open(argv[1], 'rb') as f:
    file = f.read()
nb = ""
side_size = int(sqrt(len(file) / 4) * 4)
print(side_size)

for i, char in enumerate(file):
    if i != 0 and (i % side_size) == 0:
        print("")
    nb += chr(char)
    if i % 4 == 3:
        sum = 0
        for j, c in enumerate(nb[::-1]):
            sum = sum + ((64 ** j) * base_64.index(c))
        b = sum >> (8*0) & 0xff
        g = sum >> (8*1) & 0xff
        r = sum >> (8*2) & 0xff
        print(f"\x1b[48;2;{r};{g};{b}m  \x1b[0m", end="")
        nb = ""