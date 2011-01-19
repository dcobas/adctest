import math

samples = input('Number of divisions: ')

i = 0
while i <= samples:
    # do sample i
    x = 2 * math.pi * i / samples
    print math.sin(x)
    i = i + 1
