import numpy as np
from PIL import Image

# --- VARIABLES ---

# Dev Variables
#   Version 1: 21x21, Version 2: 25x25, Version 3: 29x29 ... Version 40: 177x177
DEV_QR_VERSION = 8
DEV_VIEW_SCALE_FACTOR = 32

# Format Info
FORMAT_ERROR_CORRECTION_LEVEL = 0
FORMAT_MASK_PATTERN = 0
FORMAT_DATA_MODE = 1

# Program Variables
VAR_QR_SIZE = DEV_QR_VERSION * 4 + 17

QR_CODE = Image.new(mode="1", size=(VAR_QR_SIZE, VAR_QR_SIZE), color=1)
QR_CODE_PIXELS = QR_CODE.load()


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

#   Error Correction Level


#   Mask Patterns




SCALED_QR_CODE = QR_CODE.resize((VAR_QR_SIZE * DEV_VIEW_SCALE_FACTOR, VAR_QR_SIZE * DEV_VIEW_SCALE_FACTOR), resample=Image.Resampling.NEAREST)
SCALED_QR_CODE.show()
