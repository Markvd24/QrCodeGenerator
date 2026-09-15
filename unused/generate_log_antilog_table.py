exponent_to_integer = [1]

for i in range(1, 256):
    n = 2 * exponent_to_integer[i-1]
    if n > 255:
        n ^= 285
    exponent_to_integer.append(n)

integer_to_exponent = []

for i in range(1,256):
    integer_to_exponent.append(exponent_to_integer.index(i))

print(exponent_to_integer)
print(integer_to_exponent)