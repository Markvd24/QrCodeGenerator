from __future__ import annotations
from PIL import Image
import numpy as np
from math import floor
from simple_functions import create_byte, zip_array
from constants import *

from error_correction import ErrorCorrection

class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self, allBlack:bool=True):

        self.background = self.white

        self.color_finder_pattern = (255, 0, 0)
        self.color_aligntment_pattern = (0, 255, 0)
        self.color_timing_pattern = (0, 0, 255)
        self.color_single_pixel = (255, 174, 0)
        self.color_format_information = (255, 255, 0)
        self.color_message = (100, 255, 255)

        if allBlack:
            self.color_finder_pattern = self.black
            self.color_aligntment_pattern = self.black
            self.color_timing_pattern = self.black
            self.color_single_pixel = self.black
            self.color_format_information = self.black
            self.color_message = self.black

class Analyze:
    character_capacity_per_type_level_version = [
        [[41, 77, 127, 187, 255, 322, 370, 461, 552, 652, 772, 883, 1022, 1101, 1250, 1408, 1548, 1725, 1903, 2061, 2232, 2409, 2620, 2812, 3057, 3283, 3517, 3669, 3909, 4158, 4417, 4686, 4965, 5253, 5529, 5836, 6153, 6479, 6743, 7089],
        [34, 63, 101, 149, 202, 255, 293, 365, 432, 513, 604, 691, 796, 871, 991, 1082, 1212, 1346, 1500, 1600, 1708, 1872, 2059, 2188, 2395, 2544, 2701, 2857, 3035, 3289, 3486, 3693, 3909, 4134, 4343, 4588, 4775, 5039, 5313, 5596],
        [27, 48, 77, 111, 144, 178, 207, 259, 312, 364, 427, 489, 580, 621, 703, 775, 876, 948, 1063, 1159, 1224, 1358, 1468, 1588, 1718, 1804, 1933, 2085, 2181, 2358, 2473, 2670, 2805, 2949, 3081, 3244, 3417, 3599, 3791, 3993],
        [17, 34, 58, 82, 106, 139, 154, 202, 235, 288, 331, 374,427, 468, 530, 602, 674, 746, 813, 919, 969, 1056, 1108, 1228, 1286, 1425, 1501, 1581, 1677, 1782, 1897, 2022, 2157, 2301, 2361, 2524, 2625, 2735, 2927, 3057]
        ],
        [[25, 47, 77, 114, 154, 195, 224, 279, 335, 395, 468, 535, 619, 667, 758, 854, 938, 1046, 1153, 1249, 1352, 1460, 1588, 1704, 1853, 1990, 2132, 2223, 2369, 2520, 2677, 2840, 3009, 3183, 3351, 3537, 3729, 3927, 4087, 4296],
        [20, 38, 61, 90, 122, 154, 178, 221, 262, 311, 366, 419, 483, 528, 600, 656, 734, 816, 909, 970, 1035, 1134, 1248, 1326, 1451, 1542, 1637, 1732, 1839, 1994, 2113, 2238, 2369, 2506, 2632, 2780, 2894, 3054, 3220, 3391],
        [16, 29, 47, 67, 87, 108, 125, 157, 189, 221, 259, 296, 352, 376, 426, 470, 531, 574, 644, 702, 742, 823, 890, 963, 1041, 1094, 1172, 1263, 1322, 1429, 1499, 1618, 1700, 1787, 1867, 1966, 2071, 2181, 2298, 2420],
        [10, 20, 35, 50, 64, 84, 93, 122, 143, 174, 200, 227, 259, 283, 321, 365, 408, 452, 493, 557, 587, 640, 672, 744, 779, 864, 910, 958, 1016, 1080, 1150, 1226, 1307, 1394, 1431, 1530, 1591, 1658, 1774, 1852]
        ],
        [[17, 32, 53, 78, 106, 134, 154, 192, 230, 271, 321, 367, 425, 458, 520, 586, 644, 718, 792, 858, 929, 1003, 1091, 1171, 1273, 1367, 1465, 1528, 1628, 1732, 1840, 1952, 2068, 2188, 2303, 2431, 2563, 2699, 2809, 2953],
        [14, 26, 42, 62, 84, 106, 122, 152, 180, 213, 251, 287, 331, 362, 412, 450, 504, 560, 624, 666, 711, 779, 857, 911, 997, 1059, 1125, 1190, 1264, 1370, 1452, 1538, 1628, 1722, 1809, 1911, 1989, 2099, 2213, 2331],
        [11, 20, 32, 46, 60, 74, 86, 108, 130, 151, 177, 203, 241, 258, 292, 322, 364, 394, 442, 482, 509, 565, 611, 661, 715, 751, 805, 868, 908, 982, 1030, 1112, 1168, 1228, 1283, 1351, 1423, 1499, 1579, 1663],
        [7, 14, 24, 34, 44, 58, 64, 84, 98, 119, 137, 155, 177, 194, 220, 250, 280, 310, 338, 382, 403, 439, 461, 511, 535, 593, 625, 658, 698, 742, 790, 842, 898, 958, 983, 1051, 1093, 1139, 1219, 1273]
        ]
    ]

    def __init__(self, content:str, version:int, errorCorrectionMode):
        self.content = content
        self.version = version
        self.errorCorrectionMode = errorCorrectionMode

        self.character_count = len(self.content)

    @property
    def versionIsFixed(self):
        return (self.version != 0)

    @property
    def errorCorrectionModeIsFixed(self):
        return (self.errorCorrectionMode != '')

    @property
    def minimalErrorCorrectionIndex(self):
        if not self.errorCorrectionModeIsFixed:
            return 0
        return ['L', 'M', 'Q', 'H'].index(self.errorCorrectionMode)

    def versionToSmall(self, version_index:int) -> bool:
        version_size = self.character_capacity_per_type_level_version[self.dataTypeIndex][self.minimalErrorCorrectionIndex][version_index]
        return (self.character_count > version_size)

    def errorCorrectionToHigh(self, error_correction_index) -> bool:
        error_correction_size = self.character_capacity_per_type_level_version[self.dataTypeIndex][error_correction_index][self.version - 1]
        return (self.character_count < error_correction_size)

    def findDataType(self):
        if self.content.isnumeric():
            self.dataTypeIndex = 0 # Numeric Mode
            return
        
        for char in self.content:
            if not char in alphanumeric_table:
                self.dataTypeIndex = 2 # Bit Mode
                return
            
        self.dataTypeIndex = 1 # Alphanumeric Mode

    def findVersionIndex(self):
        if self.versionIsFixed:
            return 

        for version_index in range(40):
            if self.versionToSmall(version_index):
                continue

            self.version = version_index + 1
            return

    def findErrorCorrectionLevel(self) -> None:
        if self.errorCorrectionModeIsFixed:
            return

        for error_correction_index, error_correction_level in reversed(list(enumerate(['L', 'M', 'Q', 'H']))):
            if self.errorCorrectionToHigh(error_correction_index):
                continue

            self.errorCorrectionMode = error_correction_level
            return

    
    def find(self) -> tuple[int, int, str]:
        self.findDataType()
        self.findVersionIndex()
        self.findErrorCorrectionLevel()

        return self.dataTypeIndex, self.version, self.errorCorrectionMode

class DataType:
    def __init__(self, dataTypeIndex:int):
        self.dataType = [1, 2, 4][dataTypeIndex]

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

class MessageGenerator:
    def __init__(self, _qrCode:QrCode):
        self.version:int = _qrCode.version
        self.dataType:DataType = _qrCode.dataType
        self.errorCorrection:ErrorCorrection = _qrCode.errorCorrection
        self.content:str = _qrCode.content

        self.bitString:str = ""

    def _characterCounterValue(self):
        return len(self.content)
    
    def _characterCounterLength(self):
        version_index = floor((self.version + 7) / 17)
        mode_index = self.dataType.index
        return [[10, 9, 8], [12, 11, 16], [14, 13, 16]][version_index][mode_index]

    @property
    def characterCountIndicator(self) -> str:
        value = self._characterCounterValue()
        length = self._characterCounterLength()
        return create_byte(value, length)

    def generateBitString(self):
        encodedContent = self.dataType.encode(self.content)
        self.bitString = self.dataType.bit_string_bits + self.characterCountIndicator + encodedContent
        self.extendBitString()

    def _extendWithMax4(self):
        for _ in range(4):
            if len(self.bitString) == self.total_data_bits:
                return
            self.bitString += '0'
    
    def _extendTillMultipleOf8(self):
        while len(self.bitString) % 8 != 0:
            self.bitString += '0'
    
    def _extendWithFillerNumbers(self):
        TwohundredThirtySix = True

        while len(self.bitString) < self.total_data_bits:
            if TwohundredThirtySix:
                self.bitString += create_byte(236, 8)
            else:
                self.bitString += create_byte(17, 8)
            TwohundredThirtySix = not TwohundredThirtySix

    def extendBitString(self):
        self.total_data_bits = self.errorCorrection.error_correction_information[0] * 8

        self._extendWithMax4()
        self._extendTillMultipleOf8()
        self._extendWithFillerNumbers()
        

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

class Img:
    def __init__(self, _qrCode:QrCode):
        self.version:int = _qrCode.version
        self.dataType:DataType = _qrCode.dataType
        self.errorCorrection:ErrorCorrection = _qrCode.errorCorrection
        self.content:str = _qrCode.content

        self.mask:int = _qrCode.mask
        self.message:str = _qrCode.message
        
        self.colors = Colors()
        self.image = Image.new(mode="RGB", size=(self.qrPixels, self.qrPixels), color=self.colors.background)

        self.alignment_pattern_coords = alignment_pattern_coordinates[self.version]

    @property
    def qrPixels(self):
        return self.version * 4 + 17

    def _placeFinderPatterns(self):
        #   Top Left
        self.image.paste(self.colors.color_finder_pattern, (0,0,7,7))
        self.image.paste(self.colors.background, (1,1,6,6))
        self.image.paste(self.colors.color_finder_pattern, (2,2,5,5))
        #   Top Right
        self.image.paste(self.colors.color_finder_pattern, (self.qrPixels - 7,0,self.qrPixels,7))
        self.image.paste(self.colors.background, (self.qrPixels - 6,1,self.qrPixels - 1,6))
        self.image.paste(self.colors.color_finder_pattern, (self.qrPixels - 5,2,self.qrPixels - 2,5))
        #   Bottom Right
        self.image.paste(self.colors.color_finder_pattern, (0,self.qrPixels - 7,7,self.qrPixels))
        self.image.paste(self.colors.background, (1,self.qrPixels - 6,6,self.qrPixels - 1))
        self.image.paste(self.colors.color_finder_pattern, (2,self.qrPixels - 5,5,self.qrPixels - 2))
    
    def _placeTimingPatterns(self):
        for x in range(8, self.qrPixels - 7):
            self.image.putpixel((x,6), self.colors.background if x%2 else self.colors.color_timing_pattern)

        for y  in range(8, self.qrPixels - 7):
            self.image.putpixel((6,y), self.colors.background if y%2 else self.colors.color_timing_pattern)

    def _placeBlackPixel(self):
        self.image.putpixel((8, self.qrPixels - 8), self.colors.color_single_pixel)

    def _isValidPlaceForAlignmentPattern(self, x_index, y_index, alignment_pattern_coords):
        last = len(alignment_pattern_coords) - 1
        if x_index != 0 and x_index != last:
            return True
        if y_index != 0 and y_index != last:
            return True
        
        if x_index == last and y_index == last:
            return True

        return False
    
    def _placeAlignmentPatterns(self):
        for x_index, x in enumerate(self.alignment_pattern_coords):
            for y_index, y in enumerate(self.alignment_pattern_coords):
                if not self._isValidPlaceForAlignmentPattern(x_index, y_index, self.alignment_pattern_coords):
                    continue
                self.image.paste(self.colors.color_aligntment_pattern, (x-2,y-2,x+3,y+3))
                self.image.paste(self.colors.background, (x-1,y-1,x+2,y+2))
                self.image.putpixel((x,y), self.colors.color_aligntment_pattern)
    
    def placeFixedObjects(self):
        self._placeFinderPatterns()
        self._placeTimingPatterns()
        self._placeBlackPixel()
        self._placeAlignmentPatterns()


    @staticmethod
    def max_step_dist(A, B):
        return max(abs(A[0] - B[0]), abs(A[1] - B[1]))

    def is_data_or_ec(self, x, y):
        # Timing Patterns
        if x == 6 or y == 6:
            return False

        # Finder Patterns & Format Information Area
        dist_to_corners = [self.max_step_dist([x, y], corner) for corner in [[1, 1], [self.qrPixels-1, 1], [1, self.qrPixels-1]]]
        if min(dist_to_corners) <= 7:
            return False

        # Alignment Patterns
        for x_index, X in enumerate(self.alignment_pattern_coords):
            for y_index, Y in enumerate(self.alignment_pattern_coords):
                if (x_index == 0 or x_index == len(self.alignment_pattern_coords) - 1) and (y_index == 0 or y_index == len(self.alignment_pattern_coords) - 1) and not (x_index == len(self.alignment_pattern_coords) - 1 and y_index == len(self.alignment_pattern_coords) - 1):
                            continue
                if self.max_step_dist([x, y], [X, Y]) <= 2:
                    return False

        # Version Information Area
        if self.version < 7:
            return True

        dist_to_corners = [self.max_step_dist([x, y], corner) for corner in [[0, self.qrPixels-6], [self.qrPixels-6, 0]]]
        if min(dist_to_corners) <= 5:
            return False

        return True

    def place(self, x, y):   
        self.image.putpixel((x,y), self.colors.background if self.messageTodo.pop(0) else self.colors.color_message)

    def fill_step(self, Y):
        for i in range(2):
            dx = -(i%2)

            x = self.X+dx
            y = Y

            if not self.is_data_or_ec(x,y):
                continue

            self.place(x, y)

    def fill_column_up(self):
        for Y in reversed(range(0, self.qrPixels)):
            self.fill_step(Y)

    def fill_column_down(self):
        for Y in range(0, self.qrPixels):
            self.fill_step(Y)

    def onTimingPatterColumn(self) -> bool:
        return (self.X == 6)

    def placeMessage(self):
        self.messageTodo = [(bit == '1') for bit in self.message]

        self.X = self.qrPixels - 1
        going_up = True

        while self.X > 0:
            if going_up:
                self.fill_column_up()
            else:
                self.fill_column_down()

            going_up = not going_up
            self.X -= 2

            if self.onTimingPatterColumn():
                self.X -= 1

    def build(self):
        self.placeFixedObjects()
        self.placeMessage()

    @staticmethod
    def maskFormula(i, x, y):
        match i:
            case 0:
                return not ((x + y) % 2)
            case 1:
                return not (y % 2)
            case 2:
                return not (x % 3)
            case 3:
                return not ((x + y) % 3)
            case 4:
                return not ((floor(x/3) + floor(y/3)) % 2)
            case 5:
                return not ((x * y) % 2 + (x * y) % 3)
            case 6:
                return not (((x * y) % 2 + (x * y) % 3) % 2)
            case 7:
                return not (((x + y) % 2 + (x * y) % 3) % 2)
            
    def maskBit(self, x, y):
        bit = 0 if self.image.getpixel((x,y)) == self.colors.background else 1
        if self.is_data_or_ec(x,y) and self.maskFormula(self.mask, x, y):
            return 1-bit
        return bit

    @staticmethod
    def sign(x):
        return 1 if x>0 else -1

    def applyMask(self):
        for x in range(self.qrPixels):
            for y in range(self.qrPixels):
                if self.is_data_or_ec(x, y):
                    self.image.putpixel((x,y), self.colors.color_message if self.maskBit(x, y) == 0 else self.colors.background)
    

    # Format Information
    def format_string(self):
        generator = 0b10100110111
        format_information_mask = 0b101010000010010

        format_information = (self.errorCorrection.format_information_bits << 3) | self.mask

        format_information_error_correction = format_information << 10

        while format_information_error_correction >= (1<<10):
            padded_generator = generator << (floor(np.log2(format_information_error_correction)) - 10)
            format_information_error_correction ^= padded_generator

        format_information_encoded = (format_information << 10) | format_information_error_correction
        format_information_encoded ^= format_information_mask

        return create_byte(format_information_encoded, 15)

    def placeFormatInformation(self):
        format_information_coordinates = {
            0: [(0,8), (8,self.qrPixels-1)],
            1: [(1,8), (8,self.qrPixels-2)],
            2: [(2,8), (8,self.qrPixels-3)],
            3: [(3,8), (8,self.qrPixels-4)],
            4: [(4,8), (8,self.qrPixels-5)],
            5: [(5,8), (8,self.qrPixels-6)],
            6: [(7,8), (8,self.qrPixels-7)],
            7: [(8,8), (self.qrPixels-8,8)],
            8: [(8,7), (self.qrPixels-7,8)],
            9: [(8,5), (self.qrPixels-6,8)],
            10: [(8,4), (self.qrPixels-5,8)],
            11: [(8,3), (self.qrPixels-4,8)],
            12: [(8,2), (self.qrPixels-3,8)],
            13: [(8,1), (self.qrPixels-2,8)],
            14: [(8,0), (self.qrPixels-1,8)]
        }
        format_information_encoded = self.format_string()

        for i in range(15):
            a, b = format_information_coordinates[i]
            self.image.putpixel(b, self.colors.color_format_information if format_information_encoded[i] == "1" else self.colors.background)
            self.image.putpixel(a, self.colors.color_format_information if format_information_encoded[i] == "1" else self.colors.background)

    def finish(self):
        self.applyMask()
        self.placeFormatInformation()

    def show(self):
        PADDED_QR_CODE = Image.new(self.image.mode, (self.qrPixels + 8, self.qrPixels + 8), self.colors.background)
        PADDED_QR_CODE.paste(self.image, (4, 4))
        PADDED_QR_CODE.show()
    

class QrCode:
    def __init__(self, _version:int, _errorCorrectionMode:str, _dataTypeIndex:int, _content:str, _mask:int) -> None:
        self.version = _version
        self.dataType = DataType(_dataTypeIndex)
        self.errorCorrection = ErrorCorrection(_errorCorrectionMode, self.version, self.dataType)
        self.content = _content
        self.mask = _mask

        self.message = ""

        self.image:Img = None
        

    @classmethod
    def New(cls, content:str, inVersion:int = 0, inErrorCorrectionMode:str = '', mask:int = -1) -> QrCode:           
        Analyzer = Analyze(content, inVersion, inErrorCorrectionMode)

        dataTypeIndex, version, errorCorrectionMode = Analyzer.find()
        
        return cls(version, errorCorrectionMode, dataTypeIndex, content, mask)

    def generateMessage(self):
        self.message = MessageGenerator(self).Generate()

    def generateUnmaskedImg(self):
        self.image = Img(self)
        self.image.build()
        
    
    def testMasks(self):
        ...

    def finishImg(self):
        self.image.finish()

    def Generate(self):
        self.generateMessage()
        self.generateUnmaskedImg()
        self.testMasks()
        self.finishImg()
        self.image.show()

    
    def __str__(self) -> str:
        return f"version: {self.version}, " + f"errorCorrectionMode: {self.errorCorrection}, " + f"dataType: {self.dataType}, " + f"content: {self.content}"

    

def main():
    qr = QrCode.New("Banaantje")
    qr.Generate()
    print(qr)

if __name__ == "__main__":
    main()