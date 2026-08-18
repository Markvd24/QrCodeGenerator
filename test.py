import bchlib

BCH_POLYNOMIAL = 1335
BCH_BITS = 15

bch = bchlib.BCH(BCH_POLYNOMIAL, BCH_BITS)

print(bch.encode(13))