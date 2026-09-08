from simple_functions import extend_left
from program_variables import alphanumeric_table

def encode_alphanumeric(text):
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