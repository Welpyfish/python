import math

pi = 0

for i in range(0, 10):
    pi += (3 * math.comb(2 * i, i))/((16 ** i)(2 * i + 1))

print(pi)