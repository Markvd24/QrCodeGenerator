from __init__ import *

from alphanumeric_encoding import encode_alphanumeric

QR_CODE = Image.new(mode="1", size=(VAR_QR_SIZE, VAR_QR_SIZE), color=1)
QR_CODE_PIXELS = QR_CODE.load()

#region --- STEP 1 --- Data Analysis

#   Implement automatic selection of QR_CODE_MODE

#endregion


#region --- STEP 2 --- Data Encoding
#endregion


#region --- STEP 3 --- Error Correction Coding
#endregion


#region --- STEP 4 --- Strtucture Final Message
#endregion


#region --- STEP 5 --- Module Placement in Matrix

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

QR_CODE_PIXELS[8, VAR_QR_SIZE - 8] = 0

# Alignment Patterns
alignment_pattern_coords = alignment_pattern_coordinates[QR_CODE_VERSION]

for x_index, x in enumerate(alignment_pattern_coords):
    for y_index, y in enumerate(alignment_pattern_coords):
        if (x_index == 0 or x_index == len(alignment_pattern_coords) - 1) and (y_index == 0 or y_index == len(alignment_pattern_coords) - 1) and not (x_index == len(alignment_pattern_coords) - 1 and y_index == len(alignment_pattern_coords) - 1):
            continue
        QR_CODE.paste(0, (x-2,y-2,x+3,y+3))
        QR_CODE.paste(1, (x-1,y-1,x+2,y+2))
        QR_CODE_PIXELS[x,y] = 0

#endregion


#region --- STEP 6 --- Data Masking

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

#endregion


#region --- STEP 7 --- Format and Version Information

# Format Information
def format_string(ERROR_CORRECTION_LEVEL, MASK_PATTERN):
    format_error_correction_bin ={
        'L': 0b01,
        'M': 0b00,
        'Q': 0b11,
        'H': 0b10
    }

    generator = 0b10100110111
    format_information_mask = 0b101010000010010

    format_information = (format_error_correction_bin[FORMAT_ERROR_CORRECTION_LEVEL] << 3) | FORMAT_MASK_PATTERN

    format_information_error_correction = format_information << 10

    while format_information_error_correction >= (1<<10):
        padded_generator = generator << (floor(np.log2(format_information_error_correction)) - 10)
        format_information_error_correction ^= padded_generator

    format_information_encoded = (format_information << 10) | format_information_error_correction
    format_information_encoded ^= format_information_mask

    return bin(format_information_encoded)[2:]

format_information_encoded = format_string(FORMAT_ERROR_CORRECTION_LEVEL, FORMAT_MASK_PATTERN)

for i in range(15):
    a, b = format_information_coordinates[i]
    QR_CODE_PIXELS[a] = int(format_information_encoded[i])
    QR_CODE_PIXELS[b] = int(format_information_encoded[i])

# Content
character_count_indicator = extend_left(len(CONTENT), 9)
encoded_data = encode_alphanumeric(CONTENT)

#endregion


#region --- STEP 8 --- Display

# Display
SCALED_QR_CODE = QR_CODE.resize((VAR_QR_SIZE * DEV_VIEW_SCALE_FACTOR, VAR_QR_SIZE * DEV_VIEW_SCALE_FACTOR), resample=Image.Resampling.NEAREST)
SCALED_QR_CODE.show()

#endregion

