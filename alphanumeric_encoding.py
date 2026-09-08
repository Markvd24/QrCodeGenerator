
def extend_left(num, length):
    x = bin(num)[2:]
    return "0" * (length-len(x)) + x

def encode_alphanumeric(text):
    alphanumeric_table = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'A': 10,
        'B': 11,
        'C': 12,
        'D': 13,
        'E': 14,
        'F': 15,
        'G': 16,
        'H': 17,
        'I': 18,
        'J': 19,
        'K': 20,
        'L': 21,
        'M': 22,
        'N': 23,
        'O': 24,
        'P': 25,
        'Q': 26,
        'R': 27,
        'S': 28,
        'T': 29,
        'U': 30,
        'V': 31,
        'W': 32,
        'X': 33,
        'Y': 34,
        'Z': 35,
        ' ': 36,
        '$': 37,
        '%': 38,
        '*': 39,
        '+': 40,
        '-': 41,
        '.': 42,
        '/': 43,
        ':': 44
    }

    encoded_text = []

    for i in range(0, len(text)-1, 2):
        char1 = alphanumeric_table[text[i]]
        char2 = alphanumeric_table[text[i+1]]
        char_sum = 45 * char1 + char2
        encoded_text.append(extend_left(char_sum,11))

    if len(text)%2 == 1:
        encoded_text.append(extend_left(alphanumeric_table[text[-1]],6))

    return encoded_text

l = encode_alphanumeric('HELLO WORLD')
print(*l)