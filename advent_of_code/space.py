from collections import Counter
import re
import sys

def get_lines():
    out = []
    with open('input12.txt', 'r') as file:
        for l in file:
            out.append(l.strip())

    return out

it = get_lines()
hc = [7, 7, 7, 7, 6, 5]
o = 0
e = 0
for x in it:
    if ': ' in x:
        e += 1
        a_s, c_s = x.split(': ')
        x, y = map(int, a_s.split('x'))
        s = sum(j * k for j, k in zip(map(int, c_s.split()), hc))
        o += 1 if x * y > s else 0

print(o, e)