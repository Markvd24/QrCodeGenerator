from math import floor
import numpy as np

FORMAT_ERROR_CORRECTION_LEVEL = 'L'
FORMAT_MASK_PATTERN = 0b010

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