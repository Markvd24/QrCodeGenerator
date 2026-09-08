def extend_left(num, length):
    x = bin(num)[2:]
    return "0" * (length-len(x)) + x