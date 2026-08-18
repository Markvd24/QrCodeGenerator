import numpy as np
from PIL import Image

# --- VARIABLES ---

# Dev Variables
#   Version 1: 21x21, Version 2: 25x25, Version 3: 29x29 ... Version 40: 177x177
DEV_QR_VERSION = 2
DEV_VIEW_SCALE_FACTOR = 32

# Format Info
FORMAT_ERROR_CORRECTION_LEVEL = 'L'
FORMAT_MASK_PATTERN = 0b001
FORMAT_DATA_MODE = 1

# Program Variables
VAR_QR_SIZE = DEV_QR_VERSION * 4 + 17

QR_CODE = Image.new(mode="1", size=(VAR_QR_SIZE, VAR_QR_SIZE), color=1)
QR_CODE_PIXELS = QR_CODE.load()


BCH = lambda key: (key<<10)

# --- PROGRAM ---

# Finder Pattern
#   Top Left
QR_CODE.paste(0, (0,0,7,7))
QR_CODE.paste(1, (1,1,6,6))
QR_CODE.paste(0, (2,2,5,5))
#   Top Right
QR_CODE.paste(0, (VAR_QR_SIZE - 7,0,VAR_QR_SIZE,7))
QR_CODE.paste(1, (VAR_QR_SIZE - 6,1,VAR_QR_SIZE - 1,6))
QR_CODE.paste(0, (VAR_QR_SIZE - 5,2,VAR_QR_SIZE - 2,5))
#   Bottom Right
QR_CODE.paste(0, (0,VAR_QR_SIZE - 7,7,VAR_QR_SIZE))
QR_CODE.paste(1, (1,VAR_QR_SIZE - 6,6,VAR_QR_SIZE - 1))
QR_CODE.paste(0, (2,VAR_QR_SIZE - 5,5,VAR_QR_SIZE - 2))


# Timing Pattern
for x in range(8, VAR_QR_SIZE - 7):
    QR_CODE_PIXELS[x,6] = x%2

for y  in range(8, VAR_QR_SIZE - 7):
    QR_CODE_PIXELS[6,y] = y%2

# Alignment Patterns
PatternLocations = {
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

PatternCoords = PatternLocations[DEV_QR_VERSION]

for x_index, x in enumerate(PatternCoords):
    for y_index, y in enumerate(PatternCoords):
        if (x_index == 0 or x_index == len(PatternCoords) - 1) and (y_index == 0 or y_index == len(PatternCoords) - 1) and not (x_index == len(PatternCoords) - 1 and y_index == len(PatternCoords) - 1):
            continue
        QR_CODE.paste(0, (x-2,y-2,x+3,y+3))
        QR_CODE.paste(1, (x-1,y-1,x+2,y+2))
        QR_CODE_PIXELS[x,y] = 0

# Format Information
format_information_coord = {
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

def get_qr_format_bits(ec_level, mask_pattern):
    # 1. Create the 5-bit data string
    # EC Level: L=01, M=00, Q=11, H=10
    ec_bits = { 'L': 0b01, 'M': 0b00, 'Q': 0b11, 'H': 0b10 }[ec_level]
    data = (ec_bits << 3) | mask_pattern  # Shift EC left by 3, add mask
    
    # 2. Calculate BCH parity (divide by 10100110111)
    # Generator polynomial: 0x537 (10100110111)
    generator = 0x537
    remainder = data << 10  # Shift left by 10 to make room for parity
    
    for i in range(4, -1, -1):
        if remainder & (1 << (i + 10)):
            remainder ^= generator << i
            
    # 3. Combine data and parity
    format_info = (data << 10) | remainder
    
    # 4. XOR with the fixed mask (101010000010010) to avoid all-white modules
    format_info ^= 0x5412
    
    return format_info

format_information_encoded = np.base_repr(get_qr_format_bits(FORMAT_ERROR_CORRECTION_LEVEL, FORMAT_MASK_PATTERN), base=2)

print(format_information_encoded)

for i in range(15):
    a, b = format_information_coord[i]
    QR_CODE_PIXELS[a] = int(format_information_encoded[i])
    QR_CODE_PIXELS[b] = int(format_information_encoded[i])

# Mask
def mask(i, x, y):
    match int(str(i), 10):
        case 0:
            return not ((x + y) % 2)
        case 1:
            return not (y % 2)
        case 2:
            return not (x % 3)
        case 3:
            return not ((x + y) % 3)
        case 4:
            return not ((np.floor(x/3) + np.floor(y/3)) % 2)
        case 5:
            return not (x * y % 2 + x * y % 3)
        case 6:
            return not ((x * y % 2 + x * y % 3) % 2)
        case 7:
            return not (((x + y) % 2 + x * y % 3) % 2)


SCALED_QR_CODE = QR_CODE.resize((VAR_QR_SIZE * DEV_VIEW_SCALE_FACTOR, VAR_QR_SIZE * DEV_VIEW_SCALE_FACTOR), resample=Image.Resampling.NEAREST)
SCALED_QR_CODE.show()
