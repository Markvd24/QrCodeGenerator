from __future__ import annotations
from PIL import Image
import numpy as np
from math import floor, ceil
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
    def __init__(self, content:str, version:int, errorCorrectionMode):
        self.content = content
        self.version = version
        self.errorCorrectionMode = errorCorrectionMode

        self.versionIsFixed = (version != 0)
        self.errorCorrectionModeIsFixed = (errorCorrectionMode != '')

        self.character_count = len(self.content)

    @property
    def minimalErrorCorrectionIndex(self):
        if not self.errorCorrectionModeIsFixed:
            return 0
        return ['L', 'M', 'Q', 'H'].index(self.errorCorrectionMode)

    def versionToSmall(self, version_index:int) -> bool:
        version_size = character_capacity_per_mode_level_version[self.dataTypeIndex][self.minimalErrorCorrectionIndex][version_index]
        return (self.character_count > version_size)

    def errorCorrectionToHigh(self, error_correction_index) -> bool:
        error_correction_size = character_capacity_per_mode_level_version[self.dataTypeIndex][error_correction_index][self.version - 1]
        return (self.character_count > error_correction_size)

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

        self.totalDataBits = self.errorCorrection.totalDataCodewords * 8

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
            if len(self.bitString) >= self.totalDataBits:
                return
            self.bitString += '0'
    
    def _extendTillMultipleOf8(self):
        lastByteSize = len(self.bitString) % 8
        if lastByteSize == 0:
            return
        
        extraBitsNeeded = 8 - lastByteSize
        self.bitString += '0' * extraBitsNeeded
    
    def _extendWithFillerNumbers(self):
        TwoHundredThirtySix = True
        while len(self.bitString) < self.totalDataBits:
            if TwoHundredThirtySix:
                self.bitString += create_byte(236, 8)
            else:
                self.bitString += create_byte(17, 8)
            TwoHundredThirtySix = not TwoHundredThirtySix

    def extendBitString(self):
        self._extendWithMax4()
        self._extendTillMultipleOf8()
        self._extendWithFillerNumbers()
        

    def generateErrorCorrection(self):
        self.dataCodewords, self.errorCorrectionCodewords = self.errorCorrection.generateErrorCorrectionCodewords(self.bitString)
        
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
        if not self.hasVersionInformation:
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
                return ((x + y) % 2 == 0)
            case 1:
                return (y % 2 == 0)
            case 2:
                return (x % 3 == 0)
            case 3:
                return ((x + y) % 3 == 0)
            case 4:
                return ((floor(x/3) + (floor(y/2)) % 2) == 0)
            case 5:
                return (((x * y) % 2) + ((x * y) % 3) == 0)
            case 6:
                return ((((x * y) % 2) + ((x * y) % 3)) % 2 == 0)
            case 7:
                return ((((x + y) % 2) + ((x * y) % 3)) % 2 == 0)
            
    def maskBit(self, x, y, mask):
        bit = 0 if self.image.getpixel((x,y)) == self.colors.background else 1
        if self.is_data_or_ec(x,y) and self.maskFormula(mask, x, y):
            return 1-bit
        return bit

    @staticmethod
    def sign(x):
        return 1 if x>0 else -1

    def applyMask(self, mask):
        for x in range(self.qrPixels):
            for y in range(self.qrPixels):
                if self.is_data_or_ec(x, y):
                    self.image.putpixel((x,y), self.colors.color_message if self.maskBit(x, y, mask) == 0 else self.colors.background)
    

    # Format Information
    def generateFormatString(self, mask):
        generator = 0b10100110111
        format_information_mask = 0b101010000010010

        format_information = (self.errorCorrection.format_information_bits << 3) | mask

        format_information_error_correction = format_information << 10

        while format_information_error_correction >= (1<<10):
            padded_generator = generator << (floor(np.log2(format_information_error_correction)) - 10)
            format_information_error_correction ^= padded_generator

        format_information_encoded = (format_information << 10) | format_information_error_correction
        format_information_encoded ^= format_information_mask

        self.formatString = create_byte(format_information_encoded, 15)

    def placeFormatInformation(self, mask):
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

        self.generateFormatString(mask)

        for i in range(15):
            a, b = format_information_coordinates[i]
            self.image.putpixel(b, self.colors.color_format_information if self.formatString[i] == "1" else self.colors.background)
            self.image.putpixel(a, self.colors.color_format_information if self.formatString[i] == "1" else self.colors.background)

    @property
    def hasVersionInformation(self) -> bool:
        return (self.version >= 7)

    def placeVersionInformation(self):
        if not self.hasVersionInformation:
            return

        version_information_string_dict = {
            7: "000111110010010100",
            8: "001000010110111100",
            9: "001001101010011001",
            10: "001010010011010011",
            11: "001011101111110110",
            12: "001100011101100010",
            13: "001101100001000111",
            14: "001110011000001101",
            15: "001111100100101000",
            16: "010000101101111000",
            17: "010001010001011101",
            18: "010010101000010111",
            19: "010011010100110010",
            20: "010100100110100110",
            21: "010101011010000011",
            22: "010110100011001001",
            23: "010111011111101100",
            24: "011000111011000100",
            25: "011001000111100001",
            26: "011010111110101011",
            27: "011011000010001110",
            28: "011100110000011010",
            29: "011101001100111111",
            30: "011110110101110101",
            31: "011111001001010000",
            32: "100000100111010101",
            33: "100001011011110000",
            34: "100010100010111010",
            35: "100011011110011111",
            36: "100100101100001011",
            37: "100101010000101110",
            38: "100110101001100100",
            39: "100111010101000001",
            40: "101000110001101001"
        }

        version_information_string = version_information_string_dict[self.version]

        bottom_start_x = 0
        bottom_start_y = self.qrPixels - 11
    
        for dx in range(6):
            for dy in range(3):
                index = 17 - dx * 3 - dy
                self.image.putpixel((bottom_start_x + dx, bottom_start_y + dy), self.colors.color_format_information if version_information_string[index] == '1' else self.colors.background)
    
        right_start_x = self.qrPixels - 11
        right_start_y = 0
    
        for dy in range(6):
            for dx in range(3):
                index = 17 - dy * 3 - dx
                self.image.putpixel((right_start_x + dx, right_start_y + dy), self.colors.color_format_information if version_information_string[index] == '1' else self.colors.background)

    def addPadding(self):
        qrCodePadded = Image.new(self.image.mode, (self.qrPixels + 8, self.qrPixels + 8), self.colors.background)
        qrCodePadded.paste(self.image, (4, 4))
        self.image = qrCodePadded

    @property
    def imageScaleFactor(self):
        return ceil(MINIMUM_IMAGE_SIZE / self.qrPixels)

    def addScaling(self):
        scaledSize = (self.qrPixels + 8) * self.imageScaleFactor
        self.image = self.image.resize((scaledSize, scaledSize), resample=Image.Resampling.NEAREST)

    def addPaddingAndScale(self):
        self.addPadding()
        self.addScaling()


    def finish(self, mask):
        self.applyMask(mask)
        self.placeFormatInformation(mask)
        self.placeVersionInformation()
        self.addPaddingAndScale()

    def show(self):
        self.image.show()
    
class Evaluate:
    def __init__(self, image:Img):
        self.image = image
        self.evaluation_1 = [0 for _ in range(8)]
        self.evaluation_2 = [0 for _ in range(8)]
        self.evaluation_3 = [0 for _ in range(8)]
        self.evaluation_4 = [0 for _ in range(8)]

        self.mask = 0
        self.evaluations = [0 for _ in range(8)]

    def getMaskedBit(self, x, y):
        bit = self.image.maskBit(x, y, mask=self.mask)
        return (bit == 1)

    def updatePointsEvaluation1(self):
        if self.count == 5:
            self.evaluation_1[self.mask] += 3
        elif self.count > 5:
            self.evaluation_1[self.mask] += 1

    def nextSegment(self):
        self.startState = not self.startState
        self.count = 1
    
    def longSegmentTileScript(self, x:int, y:int):
        if self.startState == self.getMaskedBit(x, y):
            self.count += 1
            self.updatePointsEvaluation1()
        else:
            self.nextSegment()
            
    def scanColumnForLongSegments(self, y:int):
        self.startState = self.getMaskedBit(0,y)
        self.count = 1

        for x in range(1, self.image.qrPixels):
            self.longSegmentTileScript(x, y)

    def scanRowForLongSegments(self, x:int):
        self.startState = self.getMaskedBit(x,0)
        self.count = 1

        for y in range(1, self.image.qrPixels):
            self.longSegmentTileScript(x, y)

    def scanTileForBlock(self, x:int, y:int):
        if x == 0 or y == 0:
            return

        if self.getMaskedBit(x, y) == self.getMaskedBit(x, y-1) == self.getMaskedBit(x-1, y) == self.getMaskedBit(x-1, y-1):
            self.evaluation_2[self.mask] += 3

    def scanSequence(self, x:int, y:int, sequence:int):
        sequencesFound = 0
        if x >= 10:
            sequencesFound += 1
            for dx in range(11):
                X = x - dx
                pattern = (sequence & (1 << dx) != 0)
                if not self.getMaskedBit(X,y) == pattern:
                    sequencesFound -= 1
                    break

        if y >= 10:
            sequencesFound += 1
            for dy in range(11):
                Y = y - dy
                pattern = (sequence & (1 << dy) != 0)
                if not self.getMaskedBit(x,Y) == pattern:
                    sequencesFound -= 1
                    break

        self.evaluation_3[self.mask] += 40 * sequencesFound
             
    def scanTileForSequence(self, x:int, y:int):
        self.scanSequence(x, y, 0b00001011101)
        self.scanSequence(x, y, 0b10111010000)

    def scanTileIfBlackTile(self, x:int, y:int):
        if self.getMaskedBit(x, y):
            self.evaluation_4[self.mask] += 1

    def scan(self):
        for x in range(self.image.qrPixels):
            self.scanRowForLongSegments(x)

            for y in range(self.image.qrPixels):
                if x == 0:
                    self.scanColumnForLongSegments(y)

                self.scanTileForBlock(x, y)
                self.scanTileForSequence(x, y)
                self.scanTileIfBlackTile(x, y)

    def calculateEvaluation4(self):
        totalSize = self.image.qrPixels ** 2
        blackPixels = self.evaluation_4[self.mask]
        whitePixels = totalSize - blackPixels

        percent = (blackPixels * 20) / whitePixels

        upper = ceil(percent) * 5
        lower = floor(percent) * 5

        first = abs(upper - 50) / 5
        second = abs(lower - 50) / 5

        value = min(first, second)

        self.evaluation_4[self.mask] = int(value) * 10

    def calculateEvaluations(self):
        self.calculateEvaluation4()

        self.evaluations[self.mask] += self.evaluation_1[self.mask]
        self.evaluations[self.mask] += self.evaluation_2[self.mask]
        self.evaluations[self.mask] += self.evaluation_3[self.mask]
        self.evaluations[self.mask] += self.evaluation_4[self.mask]

    def evaluateMask(self):
        self.scan()        
        self.calculateEvaluations()

    def getBestMask(self):
        self.image.placeVersionInformation()

        for maskIndex in range(8):
            self.mask = maskIndex

            self.image.placeFormatInformation(maskIndex)
            self.evaluateMask()

        return self.evaluations.index(min(self.evaluations))

class QrCode:
    def __init__(self, _version:int, _errorCorrectionMode:str, _dataTypeIndex:int, _content:str, _mask:int) -> None:
        self.version = _version
        self.dataType = DataType(_dataTypeIndex)
        self.errorCorrection = ErrorCorrection(_errorCorrectionMode, _version)
        self.content = _content
        self.mask = _mask

        self.message = ""

        self.image:Img 

    @classmethod
    def New(cls, content:str, inVersion:int = 0, inErrorCorrectionMode:str = '', inMask:int = -1) -> QrCode:           
        Analyzer = Analyze(content, inVersion, inErrorCorrectionMode)

        dataTypeIndex, version, errorCorrectionMode = Analyzer.find()
        
        return cls(version, errorCorrectionMode, dataTypeIndex, content, inMask)

    def generateMessage(self):
        self.message = MessageGenerator(self).Generate()

    def generateUnmaskedImg(self):
        self.image = Img(self)
        self.image.build()
    
    def testMasks(self):
        if self.mask != -1:
            return
        Evaluation = Evaluate(self.image)
        self.mask = Evaluation.getBestMask()

    def finishImg(self):
        self.image.finish(self.mask)

    def Generate(self):
        self.generateMessage()
        self.generateUnmaskedImg()
        self.testMasks()
        self.finishImg()
    
    def save(self, file_name:str):
        self.image.image.save(file_name)

    
    def __str__(self) -> str:
        return f"version: {self.version}, " + f"errorCorrectionMode: {self.errorCorrection}, " + f"dataType: {self.dataType}, " + f"content: {self.content}, " + f"mask: {self.mask}"

    

def main():
    qr = QrCode.New("HELLO WORLD")
    qr.Generate()
    qr.image.show()
    print(qr)

if __name__ == "__main__":
    main()