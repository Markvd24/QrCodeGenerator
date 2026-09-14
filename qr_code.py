from __future__ import annotations
from math import floor

alphanumeric_characters = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*', '+', '-', '.', '/', ':')
character_capacity_per_version_level_type = [
[[41, 25, 17], [34, 20, 14], [27, 16, 11], [17, 10, 7]],
[[77, 47, 32], [63, 38, 26], [48, 29, 20], [34, 20, 14]],
[[127, 77, 53], [101, 61, 42], [77, 47, 32], [58, 35, 24]],
[[187, 114, 78], [149, 90, 62], [111, 67, 46], [82, 50, 34]],
[[255, 154, 106], [202, 122, 84], [144, 87, 60], [106, 64, 44]],
[[322, 195, 134], [255, 154, 106], [178, 108, 74], [139, 84, 58]],
[[370, 224, 154], [293, 178, 122], [207, 125, 86], [154, 93, 64]],
[[461, 279, 192], [365, 221, 152], [259, 157, 108], [202, 122, 84]],
[[552, 335, 230], [432, 262, 180], [312, 189, 130], [235, 143, 98]],
[[652, 395, 271], [513, 311, 213], [364, 221, 151], [288, 174, 119]],
[[772, 468, 321], [604, 366, 251], [427, 259, 177], [331, 200, 137]],
[[883, 535, 367], [691, 419, 287], [489, 296, 203], [374, 227, 155]],
[[1022, 619, 425], [796, 483, 331], [580, 352, 241], [427, 259, 177]],
[[1101, 667, 458], [871, 528, 362], [621, 376, 258], [468, 283, 194]],
[[1250, 758, 520], [991, 600, 412], [703, 426, 292], [530, 321, 220]],
[[1408, 854, 586], [1082, 656, 450], [775, 470, 322], [602, 365, 250]],
[[1548, 938, 644], [1212, 734, 504], [876, 531, 364], [674, 408, 280]],
[[1725, 1046, 718], [1346, 816, 560], [948, 574, 394], [746, 452, 310]],
[[1903, 1153, 792], [1500, 909, 624], [1063, 644, 442], [813, 493, 338]],
[[2061, 1249, 858], [1600, 970, 666], [1159, 702, 482], [919, 557, 382]],
[[2232, 1352, 929], [1708, 1035, 711], [1224, 742, 509], [969, 587, 403]],
[[2409, 1460, 1003], [1872, 1134, 779], [1358, 823, 565], [1056, 640, 439]],
[[2620, 1588, 1091], [2059, 1248, 857], [1468, 890, 611], [1108, 672, 461]],
[[2812, 1704, 1171], [2188, 1326, 911], [1588, 963, 661], [1228, 744, 511]],
[[3057, 1853, 1273], [2395, 1451, 997], [1718, 1041, 715], [1286, 779, 535]],
[[3283, 1990, 1367], [2544, 1542, 1059], [1804, 1094, 751], [1425, 864, 593]],
[[3517, 2132, 1465], [2701, 1637, 1125], [1933, 1172, 805], [1501, 910, 625]],
[[3669, 2223, 1528], [2857, 1732, 1190], [2085, 1263, 868], [1581, 958, 658]],
[[3909, 2369, 1628], [3035, 1839, 1264], [2181, 1322, 908], [1677, 1016, 698]],
[[4158, 2520, 1732], [3289, 1994, 1370], [2358, 1429, 982], [1782, 1080, 742]],
[[4417, 2677, 1840], [3486, 2113, 1452], [2473, 1499, 1030], [1897, 1150, 790]],
[[4686, 2840, 1952], [3693, 2238, 1538], [2670, 1618, 1112], [2022, 1226, 842]],
[[4965, 3009, 2068], [3909, 2369, 1628], [2805, 1700, 1168], [2157, 1307, 898]],
[[5253, 3183, 2188], [4134, 2506, 1722], [2949, 1787, 1228], [2301, 1394, 958]],
[[5529, 3351, 2303], [4343, 2632, 1809], [3081, 1867, 1283], [2361, 1431, 983]],
[[5836, 3537, 2431], [4588, 2780, 1911], [3244, 1966, 1351], [2524, 1530, 1051]],
[[6153, 3729, 2563], [4775, 2894, 1989], [3417, 2071, 1423], [2625, 1591, 1093]],
[[6479, 3927, 2699], [5039, 3054, 2099], [3599, 2181, 1499], [2735, 1658, 1139]],
[[6743, 4087, 2809], [5313, 3220, 2213], [3791, 2298, 1579], [2927, 1774, 1219]],
[[7089, 4296, 2953], [5596, 3391, 2331], [3993, 2420, 1663], [3057, 1852, 1273]],
]
error_correction_information_per_version_mode = [
[[19, 7, 1, 19], [16, 10, 1, 16], [13, 13, 1, 13], [9, 17, 1, 9]],
[[34, 10, 1, 34], [28, 16, 1, 28], [22, 22, 1, 22], [16, 28, 1, 16]],
[[55, 15, 1, 55], [44, 26, 1, 44], [34, 18, 2, 17], [26, 22, 2, 13]],
[[80, 20, 1, 80], [64, 18, 2, 32], [48, 26, 2, 24], [36, 16, 4, 9]],
[[108, 26, 1, 108], [86, 24, 2, 43], [62, 18, 2, 15, 2, 16], [46, 22, 2, 11, 2, 12]],
[[136, 18, 2, 68], [108, 16, 4, 27], [76, 24, 4, 19], [60, 28, 4, 15]],
[[156, 20, 2, 78], [124, 18, 4, 31], [88, 18, 2, 14, 4, 15], [66, 26, 4, 13, 1, 14]],
[[194, 24, 2, 97], [154, 22, 2, 38, 2, 39], [110, 22, 4, 18, 2, 19], [86, 26, 4, 14, 2, 15]],
[[232, 30, 2, 116], [182, 22, 3, 36, 2, 37], [132, 20, 4, 16, 4, 17], [100, 24, 4, 12, 4, 13]],
[[274, 18, 2, 68, 2, 69], [216, 26, 4, 43, 1, 44], [154, 24, 6, 19, 2, 20], [122, 28, 6, 15, 2, 16]],
[[324, 20, 4, 81], [254, 30, 1, 50, 4, 51], [180, 28, 4, 22, 4, 23], [140, 24, 3, 12, 8, 13]],
[[370, 24, 2, 92, 2, 93], [290, 22, 6, 36, 2, 37], [206, 26, 4, 20, 6, 21], [158, 28, 7, 14, 4, 15]],
[[428, 26, 4, 107], [334, 22, 8, 37, 1, 38], [244, 24, 8, 20, 4, 21], [180, 22, 12, 11, 4, 12]],
[[461, 30, 3, 115, 1, 116], [365, 24, 4, 40, 5, 41], [261, 20, 11, 16, 5, 17], [197, 24, 11, 12, 5, 13]],
[[523, 22, 5, 87, 1, 88], [415, 24, 5, 41, 5, 42], [295, 30, 5, 24, 7, 25], [223, 24, 11, 12, 7, 13]],
[[589, 24, 5, 98, 1, 99], [453, 28, 7, 45, 3, 46], [325, 24, 15, 19, 2, 20], [253, 30, 3, 15, 13, 16]],
[[647, 28, 1, 107, 5, 108], [507, 28, 10, 46, 1, 47], [367, 28, 1, 22, 15, 23], [283, 28, 2, 14, 17, 15]],
[[721, 30, 5, 120, 1, 121], [563, 26, 9, 43, 4, 44], [397, 28, 17, 22, 1, 23], [313, 28, 2, 14, 19, 15]],
[[795, 28, 3, 113, 4, 114], [627, 26, 3, 44, 11, 45], [445, 26, 17, 21, 4, 22], [341, 26, 9, 13, 16, 14]],
[[861, 28, 3, 107, 5, 108], [669, 26, 3, 41, 13, 42], [485, 30, 15, 24, 5, 25], [385, 28, 15, 15, 10, 16]],
[[932, 28, 4, 116, 4, 117], [714, 26, 17, 42], [512, 28, 17, 22, 6, 23], [406, 30, 19, 16, 6, 17]],
[[1006, 28, 2, 111, 7, 112], [782, 28, 17, 46], [568, 30, 7, 24, 16, 25], [442, 24, 34, 13]],
[[1094, 30, 4, 121, 5, 122], [860, 28, 4, 47, 14, 48], [614, 30, 11, 24, 14, 25], [464, 30, 16, 15, 14, 16]],
[[1174, 30, 6, 117, 4, 118], [914, 28, 6, 45, 14, 46], [664, 30, 11, 24, 16, 25], [514, 30, 30, 16, 2, 17]],
[[1276, 26, 8, 106, 4, 107], [1000, 28, 8, 47, 13, 48], [718, 30, 7, 24, 22, 25], [538, 30, 22, 15, 13, 16]],
[[1370, 28, 10, 114, 2, 115], [1062, 28, 19, 46, 4, 47], [754, 28, 28, 22, 6, 23], [596, 30, 33, 16, 4, 17]],
[[1468, 30, 8, 122, 4, 123], [1128, 28, 22, 45, 3, 46], [808, 30, 8, 23, 26, 24], [628, 30, 12, 15, 28, 16]],
[[1531, 30, 3, 117, 10, 118], [1193, 28, 3, 45, 23, 46], [871, 30, 4, 24, 31, 25], [661, 30, 11, 15, 31, 16]],
[[1631, 30, 7, 116, 7, 117], [1267, 28, 21, 45, 7, 46], [911, 30, 1, 23, 37, 24], [701, 30, 19, 15, 26, 16]],
[[1735, 30, 5, 115, 10, 116], [1373, 28, 19, 47, 10, 48], [985, 30, 15, 24, 25, 25], [745, 30, 23, 15, 25, 16]],
[[1843, 30, 13, 115, 3, 116], [1455, 28, 2, 46, 29, 47], [1033, 30, 42, 24, 1, 25], [793, 30, 23, 15, 28, 16]],
[[1955, 30, 17, 115], [1541, 28, 10, 46, 23, 47], [1115, 30, 10, 24, 35, 25], [845, 30, 19, 15, 35, 16]],
[[2071, 30, 17, 115, 1, 116], [1631, 28, 14, 46, 21, 47], [1171, 30, 29, 24, 19, 25], [901, 30, 11, 15, 46, 16]],
[[2191, 30, 13, 115, 6, 116], [1725, 28, 14, 46, 23, 47], [1231, 30, 44, 24, 7, 25], [961, 30, 59, 16, 1, 17]],
[[2306, 30, 12, 121, 7, 122], [1812, 28, 12, 47, 26, 48], [1286, 30, 39, 24, 14, 25], [986, 30, 22, 15, 41, 16]],
[[2434, 30, 6, 121, 14, 122], [1914, 28, 6, 47, 34, 48], [1354, 30, 46, 24, 10, 25], [1054, 30, 2, 15, 64, 16]],
[[2566, 30, 17, 122, 4, 123], [1992, 28, 29, 46, 14, 47], [1426, 30, 49, 24, 10, 25], [1096, 30, 24, 15, 46, 16]],
[[2702, 30, 4, 122, 18, 123], [2102, 28, 13, 46, 32, 47], [1502, 30, 48, 24, 14, 25], [1142, 30, 42, 15, 32, 16]],
[[2812, 30, 20, 117, 4, 118], [2216, 28, 40, 47, 7, 48], [1582, 30, 43, 24, 22, 25], [1222, 30, 10, 15, 67, 16]],
[[2956, 30, 19, 118, 6, 119], [2334, 28, 18, 47, 31, 48], [1666, 30, 34, 24, 34, 25], [1276, 30, 20, 15, 61, 16]]
]

exponent_to_integer = [
    1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161, 95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240, 253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226, 217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206, 129, 31, 62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204, 133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84, 168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115, 230, 209, 191, 99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65, 130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166, 81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72, 144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1]

integer_to_exponent = [
    0, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64, 30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87, 7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46, 55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108, 161, 59, 82,41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117,44, 215, 79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175]

exp_add = lambda a, b: integer_to_exponent[exponent_to_integer[a % 255] ^ exponent_to_integer[b % 255]]
exp_to_int = lambda A: [exponent_to_integer[a] for a in A]
int_to_exp = lambda A: [integer_to_exponent[a] for a in A]

def zip_array(array: list[list]):
    zipped_array = []
    max_length = max([len(a) for a in array])
    for index in range(max_length):
        for list in array:
            if len(list) <= index:
                continue
            zipped_array.append(list[index])
    return zipped_array

def create_byte(value:int, byte_size:int=8) -> str:
    return bin(value)[2:].zfill(byte_size)

class ErrorCorrection:
    INDEX_TABLE = ['L', 'M', 'Q', 'H']

    def __init__(self, errorCorrectionMode, _version, _dataType) -> None:
        if isinstance(errorCorrectionMode, int):
            errorCorrectionMode = self.INDEX_TABLE[errorCorrectionMode]
        self.errorCorrectionMode = errorCorrectionMode

        self.error_correction_information = error_correction_information_per_version_mode[_version - 1][_dataType.index]
        self.nGroups = 1 if len(self.error_correction_information) == 4 else 2
        self.codewordsPerBlock = self.error_correction_information[1]

        self.generator_polynomial = self.generate_generator_polynomial(self.codewordsPerBlock)

        self.dataCodewords = []
        self.errorCorrectionCodewords = []

    @property
    def index(self):
        return self.INDEX_TABLE.index(self.errorCorrectionMode)

    @property
    def format_information_bits(self):
        qrcode_value = ['M', 'L', 'H', 'Q'].index(self.errorCorrectionMode)
        return create_byte(qrcode_value, 2)

    def __str__(self):
        return self.errorCorrectionMode
    
    def _generateDataCodewords(self, bitString):
        codewordsIndex = 0
        rawDataCodewords = [bitString[i:i+8] for i in range(0, len(bitString), 8)]

        for group in range(self.nGroups):
            # obtain group specs
            blocks_in_group = self.error_correction_information[2 + 2 * group]
            codewords_per_block = self.error_correction_information[3 + 2 * group]

            for _ in range(blocks_in_group):
                # Obtain the message polynomial from CODEWORDS
                message_polynomial_binary = [rawDataCodewords[codewordsIndex + cw] for cw in range(codewords_per_block)]
                codewordsIndex += codewords_per_block
        
                # Turn message_polynomial_binary to integers
                message_polynomial = [int(bite,2) for bite in message_polynomial_binary]

                self.dataCodewords.append(message_polynomial)


    @staticmethod
    def generate_generator_polynomial(type):
        # index: [a for x^type, a for x^(type-1), a for x^(type-2), ..., a for x^0]
        # So building the formula, it would be:
        # poly[0] * x^n + poly[1] * x^(n-1) + poly[2] * x^(n-2) + ... poly[n] * x^0
        
        if type <= 1:
            return [0, 0]

        previous_polynomial = ErrorCorrection.generate_generator_polynomial(type-1)

        new_polynomial = [previous_polynomial[0]]

        for i in range(type-1):
            from_x = previous_polynomial[i+1]
            from_a = previous_polynomial[i] + type - 1
            new_polynomial.append(exp_add(from_x, from_a))

        new_polynomial.append(previous_polynomial[-1] + type - 1)

        return new_polynomial

    @staticmethod
    def polynomial_long_devision(message_polynomial, generator_polynomial):
        # Step 1: Set variables
        message = message_polynomial
        generator = generator_polynomial
        message_size = len(message)
        
        # Step 2: Multiply the Message Polynomial by x^n where n is the number of codewords
        message = message + [0 for _ in range(len(generator)-1)]

        for _ in range(message_size):
            # Multiply the Generator Polynomial by the Lead Term of the Message Polynomial
            leading_term = integer_to_exponent[message[0]]
            multiplied_generator = exp_to_int([(term + leading_term) % 255 for term in generator])

            # XOR the result with the message polynomial
            for index, generator_term in enumerate(multiplied_generator):
                message[index] ^= generator_term

            if message[0] == 0:
                message.pop(0)     

        return message

    def _generateErrorCorrectionCodewords(self):
        for message_polynomial in self.dataCodewords:
            # Calculate the polynomial long devision of message_polynomial and generator_polynomial
            long_devision_result = self.polynomial_long_devision(message_polynomial, self.generator_polynomial)

            self.errorCorrectionCodewords.append(long_devision_result)

    def generateErrorCorrectionCodewords(self, bitString):
        self._generateDataCodewords(bitString)
        self._generateErrorCorrectionCodewords()
        return self.dataCodewords, self.errorCorrectionCodewords
    
class DataType:
    def __init__(self, dataType:int):
        self.dataType = dataType

    def __str__(self):
        return ["numeric", "alphanumeric", "bits"][self.index]

    @property
    def index(self) -> int:
        return [1, 2, 4].index(self.dataType)

    @property
    def bit_string_bits(self):
        return create_byte(self.dataType, 4)

    @staticmethod
    def _encode_numeric(text):
        encoded_text = []

        for index in range(3, len(text), 3):
            number = int(text[index-3:index])
            encoded_text.append(create_byte(number, 10))

        amount_extra = len(text)%3
        match amount_extra:
            case 1:
                number = int(text[-1])
                encoded_text.append(create_byte(number, 4))
            case 2:
                number = int(text[-2:])
                encoded_text.append(create_byte(number, 7))

        return encoded_text

    @staticmethod
    def _encode_alphanumeric(text):
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
            encoded_text.append(create_byte(char_sum,11))

        if len(text)%2 == 1:
            encoded_text.append(create_byte(alphanumeric_table[text[-1]],6))

        return encoded_text

    @staticmethod
    def _encode_bit(text):
        encoded_text = []

        for char in text:
            hex_value = char.encode('iso-8859-1').hex()
            
            # print(f"{char.encode('iso-8859-1')}: {hex_value}")
            encoded_text.append(create_byte(int(hex_value, 16), 8))

        return encoded_text


    def encode(self, content):
        encoded_data = []
        match self.index:
            case 0:
                encoded_data = self._encode_numeric(content)
            case 1:
                encoded_data = self._encode_alphanumeric(content)
            case 2:
                encoded_data = self._encode_bit(content)

        return "".join(encoded_data)

class QrCodeMessageGenerator:
    def __init__(self, _qrCode:QrCode):
        self.version = _qrCode.version
        self.errorCorrection = _qrCode.errorCorrection
        self.dataType = _qrCode.dataType
        self.content = _qrCode.content

        self.bitString = ""

        

    @property
    def characterCountIndicator(self) -> str:
        def counter_value(self):
            return len(self.content)
        
        def counter_length(self):
            version_index = floor((self.version + 7) / 17)
            mode_index = self.dataType.index
            return [[10, 9, 8], [12, 11, 16], [14, 13, 16]][version_index][mode_index]

        value = counter_value(self)
        length = counter_length(self)
        return create_byte(value, length)


    def generateBitString(self):
        encodedContent = self.dataType.encode(self.content)
        self.bitString = self.dataType.bit_string_bits + self.characterCountIndicator + encodedContent
        self.extendBitString()

    def extendBitString(self):
        total_data_codewords = self.errorCorrection.error_correction_information[0]
        total_data_bits = total_data_codewords * 8


        #   Add a maximum of 4 bits
        for _ in range(4):
            if len(self.bitString) == total_data_bits:
                break
            self.bitString += '0'

        #   Fill with zeros till multiple of 8
        while len(self.bitString) % 8 != 0:
            self.bitString += '0'

        #   Fill with 236 and 17 until data is fully filled
        TwohundredThirtySix = True
        while len(self.bitString) < total_data_bits:
            if TwohundredThirtySix:
                self.bitString += create_byte(236, 8)
            else:
                self.bitString += create_byte(17, 8)
            TwohundredThirtySix = not TwohundredThirtySix

    def generateErrorCorrection(self):
        self.dataCodewords, self.errorCorrectionCodewords = self.errorCorrection.generateErrorCorrectionCodewords(self.bitString)
        print("".join(["".join([create_byte(b) for b in l]) for l in self.dataCodewords]))
        print("".join(["".join([create_byte(b) for b in l]) for l in self.errorCorrectionCodewords]))
        

    def structureMessage(self):
        self.zipCodewords()
        self.convertCodewordsToBits()
        self.addLeadingZeros()

    def zipCodewords(self):
        dataCodewordsZipped = zip_array(self.dataCodewords)
        errorCorrectionCodewordsZipped = zip_array(self.errorCorrectionCodewords)
        self.messageCodewords = dataCodewordsZipped + errorCorrectionCodewordsZipped

    def convertCodewordsToBits(self):
        self.message = "".join([create_byte(codeword, 8) for codeword in self.messageCodewords])

    def addLeadingZeros(self):
        self.message += "0" * self.leadingZerosCount

    @property
    def leadingZerosCount(self):
        return 0 if self.version == 1 else (4 - (floor(self.version / 7 - 3) ** 2)) % 12

    def Generate(self) -> str:
        self.generateBitString()
        self.generateErrorCorrection()
        self.structureMessage()
        return self.message


class QrCode:
    def __init__(self, _version:int, _errorCorrectionMode:str, _dataType:int, _content:str) -> None:
        self.version = _version
        self.dataType = DataType(_dataType)
        self.errorCorrection = ErrorCorrection(_errorCorrectionMode, self.version, self.dataType)
        self.content = _content

    @classmethod
    def New(cls, _content:str, _version:int = 0, _errorCorrectionMode:str = '') -> QrCode:           
        
        def findDataType(content: str) -> DataType:
            modeIndicator = 0b0001 # Numeric Mode

            if not content.isnumeric():
                modeIndicator = 0b0010 # Alphanumeric Mode
                for char in content:
                    if alphanumeric_characters.count(char):
                        continue
                    modeIndicator = 0b0100 # Bit Mode
                    break
            return DataType(modeIndicator)

        def findVersionAndErrorCorrectionMode(content:str, version, errorCorrectionMode, dataType:DataType) -> tuple[int, str]:
            character_count = len(content)
            FoundSmallestQR = False
            version_index = 0
            error_correction_level = 'L'
            mode_index = dataType.index

            error_correction_modes = ['L', 'M', 'Q', 'H']
            if errorCorrectionMode != '':
                error_correction_modes = [errorCorrectionMode]
    
            while not FoundSmallestQR:
                for local_error_correction_level_index, _error_correction_level in reversed(list(enumerate(error_correction_modes))):
                    if character_count <= character_capacity_per_version_level_type[version_index][local_error_correction_level_index][mode_index]:
                        FoundSmallestQR = True
                        error_correction_level = _error_correction_level
                        break
    
                version_index += 1

            return version_index, error_correction_level

        content = _content
        dataType = findDataType(content)
        version, errorCorrectionMode = findVersionAndErrorCorrectionMode(content, _version, _errorCorrectionMode, dataType)
        
        return cls(version, errorCorrectionMode, dataType.dataType, content)

    def Generate(self):
        message = QrCodeMessageGenerator(self).Generate()
        print(message)
    
    def __str__(self) -> str:
        return f"version: {self.version}, " + f"errorCorrectionMode: {self.errorCorrection}, " + f"dataType: {self.dataType}, " + f"content: {self.content}"

    
    
qr = QrCode.New("Banaantje")
qr.Generate()
print(qr)