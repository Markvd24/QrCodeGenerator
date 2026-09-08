from config import *
import numpy as np
from math import *


# Program Variables
VAR_QR_SIZE = QR_CODE_VERSION * 4 + 17


# CHARACTER_COUNT_INDICATOR_LENGTH
CHARACTER_COUNT_INDICATOR_LENGTH = [[10, 9, 8], [12, 11, 16], [14, 13, 16]][floor((QR_CODE_VERSION + 7) / 17), np.log2(QR_CODE_MODE_INDICATOR)]


# Dictionaries
alignment_pattern_coordinates = {
    1: [],
    2: [6,18],
    3: [6,22],
    4: [6,26],
    5: [6,30],
    6: [6,34],
    7: [6,22,38],
    8: [6,24,42],
    9: [6,26,46],
    10: [6,28,50],
    11: [6,30,54],
    12: [6,32,58],
    13: [6,43,62],
    14: [6,26,46,66]
}

format_information_coordinates = {
    0: [(0,8), (8,VAR_QR_SIZE-1)],
    1: [(1,8), (8,VAR_QR_SIZE-2)],
    2: [(2,8), (8,VAR_QR_SIZE-3)],
    3: [(3,8), (8,VAR_QR_SIZE-4)],
    4: [(4,8), (8,VAR_QR_SIZE-5)],
    5: [(5,8), (8,VAR_QR_SIZE-6)],
    6: [(7,8), (8,VAR_QR_SIZE-7)],
    7: [(8,8), (VAR_QR_SIZE-8,8)],
    8: [(8,7), (VAR_QR_SIZE-7,8)],
    9: [(8,5), (VAR_QR_SIZE-6,8)],
    10: [(8,4), (VAR_QR_SIZE-5,8)],
    11: [(8,3), (VAR_QR_SIZE-4,8)],
    12: [(8,2), (VAR_QR_SIZE-3,8)],
    13: [(8,1), (VAR_QR_SIZE-2,8)],
    14: [(8,0), (VAR_QR_SIZE-1,8)]
}

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

