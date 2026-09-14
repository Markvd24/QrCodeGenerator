from math import *
from PIL import Image
import numpy as np

from encoding import *
from simple_functions import extend_left


#region --- INIT VARIABLES ---

DEV_VIEW_SCALE_FACTOR = 32

#   Version 1: 21x21, Version 2: 25x25, Version 3: 29x29 ... Version 40: 177x177


# Format Info


CONTENT = """Alright, my brothers, listen closely
Tonight, we make the Trojans pay
Ten years of war, they've killed us slowly
But now we'll be the ones who slay
Think of your wives and your children
Your families wonder where you've been
They're growing old and yet you're still here
Do what I say, and you'll see them again (yes, sir!)
Diomedes will lead the charge
Agamemnon will flank the guards
Menelaus will let our mates
Through the gates to take the whole city at large
Teucer will shoot any ambush attack
And little Ajax will stay back
Nestor, secure Helen and protect her
Neo, avenge your father, kill the brothers of Hector (yes, sir!)
Find that inner strength now (whoo!)
Use that well of pride (whoo!)
Fight through every pain now (whoo!)
Ask yourself inside
What do you live for? What do you try for?
What do you wish for? What do you fight for?
(What do you live for? What do you try for?)
(What do you wish for? What do you fight for?)
Penelope
Penelope
And Telemachus
I fight for us
I fight for us
Penelope
(What do you try for?) Telemachus
(What do you wish for?) I'm on my way
(What do you fight for?) Attack!
Who was that?
A vision
Of what is to come, cannot be outrun
Can only be dealt with right here and now
Tell me how
I don't think you're ready
A mission to kill someone's son
A foe who won't run
Unlike anyone you have faced before
Say no more
I know that I'm ready
(I don't think you're ready)
It's just an infant
It's just a boy
What sort of imminent threat does he pose, that I cannot avoid?
This is the son of none other than Troy's very own Prince Hector
Know that he will grow from a boy to an avenger
One fueled with rage as you're consumed by age
If you don't end him now, you'll have no one left to save
You can say goodbye to (Penelope)
You can say goodbye to (Penelope)
I could raise him as my own (he will burn your house and throne)
Or send him far away from home (he'll find you wherever you go)
Make sure his past is never known (the gods will make him know)
I'd rather bleed for ya (he's bringing you)
Down on my knees for ya
I'm begging please (oh, this is the will of the gods)
Please don't make me do this, don't make me do this
The blood on your hands is something you won't lose
All you can choose is whose"""

CONTENT = "Banaantje"

FORCE_FORMAT = 0
QR_CODE_VERSION = 1
ERROR_CORRECTION_LEVEL = 0
MASK_PATTERN = 0

# CONTENT = input("What is the content? ")

# Program Variables

# Dictionaries


#endregion


#region --- STEP 1 --- Data Analysis

alphanumeric_characters = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*', '+', '-', '.', '/', ':')

MODE_INDICATOR = 0b0001 # Numeric Mode

if not CONTENT.isnumeric():
    MODE_INDICATOR = 0b0010 # Alphanumeric Mode
    for char in CONTENT:
        if alphanumeric_characters.count(char):
            continue
        MODE_INDICATOR = 0b0100 # Bit Mode
        break

character_capacity_per_version_level_mode = [
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


character_amount = len(CONTENT)
FoundSmallestQR = False
version_index = 0
level_index = 0
mode_index = floor(np.log2(MODE_INDICATOR))

while not FoundSmallestQR:
    for local_level_index, error_correction_level in reversed(list(enumerate(['L', 'M', 'Q', 'H']))):
        if character_amount <= character_capacity_per_version_level_mode[version_index][local_level_index][mode_index]:
            FoundSmallestQR = True
            level_index = local_level_index
            break

    version_index += 1

if FORCE_FORMAT:
    version_index = QR_CODE_VERSION
    level_index = ERROR_CORRECTION_LEVEL
QR_CODE_VERSION = version_index
ERROR_CORRECTION_LEVEL = ['L', 'M', 'Q', 'H'][level_index]

#endregion


#region --- STEP 2 --- Data Encoding

CHARACTER_COUNT_INDICATOR_LENGTH = [[10, 9, 8], [12, 11, 16], [14, 13, 16]][floor((QR_CODE_VERSION + 7) / 17)][floor(np.log2(MODE_INDICATOR))]
CHARACTER_COUNT_INDICATOR = extend_left(len(CONTENT), CHARACTER_COUNT_INDICATOR_LENGTH)

if MODE_INDICATOR == 0b0001:
    ENCODED_DATA = encode_numeric(CONTENT)
elif MODE_INDICATOR == 0b0010:
    ENCODED_DATA = encode_alphanumeric(CONTENT)
elif MODE_INDICATOR == 0b0100:
    ENCODED_DATA = encode_bit(CONTENT)
else:
    ENCODED_DATA = ''

print(MODE_INDICATOR)
print(CHARACTER_COUNT_INDICATOR)

BIT_STRING = extend_left(MODE_INDICATOR, 4) + CHARACTER_COUNT_INDICATOR + ''.join(ENCODED_DATA)


#   [total number of data words, EC codewords per block, number of blocks in group 1, number of codewords in each group 1 block, number of blocks in group 2, number of codewords in each group 2 block]
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

error_correction_information = error_correction_information_per_version_mode[QR_CODE_VERSION - 1][level_index]

total_data_codewords = error_correction_information[0]
total_data_bits = total_data_codewords * 8


#   Add a maximum of 4 bits
for _ in range(4):
    if len(BIT_STRING) == total_data_bits:
        break
    BIT_STRING += '0'

#   Fill with zeros till multiple of 8
while len(BIT_STRING) % 8 != 0:
    BIT_STRING += '0'

#   Fill with 236 and 17 until data is fully filled
TwohundredThirtySix = True
while len(BIT_STRING) < total_data_bits:
    if TwohundredThirtySix:
        BIT_STRING += extend_left(236, 8)
    else:
        BIT_STRING += extend_left(17, 8)
    TwohundredThirtySix = not TwohundredThirtySix

#endregion
print(f"QR_CODE_VERSION: {QR_CODE_VERSION}")
print(f"ERROR_CORRECTION_LEVEL: {ERROR_CORRECTION_LEVEL}")
print(f"total_data_bits: {total_data_bits}")
print(f"MODE_INDICATOR: {MODE_INDICATOR}")


#region --- STEP 3 --- Error Correction Coding
exponent_to_integer = [
    1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152, 45, 90, 180, 117, 234, 201, 143, 3, 6, 12, 24, 48, 96, 192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70, 140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161, 95, 190, 97, 194, 153, 47, 94, 188, 101, 202, 137, 15, 30, 60, 120, 240, 253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182, 113, 226, 217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206, 129, 31, 62, 124, 248, 237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204, 133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66, 132, 21, 42, 84, 168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115, 230, 209, 191, 99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171, 75, 150, 49, 98, 196, 149, 55, 110, 220, 165, 87, 174, 65, 130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166, 81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72, 144, 61, 122, 244, 245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173, 71, 142, 1]

integer_to_exponent = [
    0, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181, 194, 125, 106, 39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145, 34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64, 30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87, 7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 32, 137, 46, 55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108, 161, 59, 82,41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117,44, 215, 79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175]

exp_add = lambda a, b: integer_to_exponent[exponent_to_integer[a % 255] ^ exponent_to_integer[b % 255]]
exp_to_int = lambda A: [exponent_to_integer[a] for a in A]
int_to_exp = lambda A: [integer_to_exponent[a] for a in A]

def generate_generator_polynomial(type):
    # index: [a for x^type, a for x^(type-1), a for x^(type-2), ..., a for x^0]
    # So building the formula, it would be:
    # poly[0] * x^n + poly[1] * x^(n-1) + poly[2] * x^(n-2) + ... poly[n] * x^0
    
    if type <= 1:
        return [0, 0]

    previous_polynomial = generate_generator_polynomial(type-1)

    new_polynomial = [previous_polynomial[0]]

    for i in range(type-1):
        from_x = previous_polynomial[i+1]
        from_a = previous_polynomial[i] + type - 1
        new_polynomial.append(exp_add(from_x, from_a))

    new_polynomial.append(previous_polynomial[-1] + type - 1)

    return new_polynomial

def polynomial_long_devision(message_polynomial, generator_polynomial):
    # Step 1: Set variables
    message = message_polynomial
    generator = generator_polynomial
    message_size = len(message)
    
    # Step 2: Multiply the Message Polynomial by x^n where n is the number of codewords
    message = message + [0 for _ in range(len(generator)-1)]
    print(len(generator))
    print(generator)
    print(message)

    for a in range(message_size):
        # Multiply the Generator Polynomial by the Lead Term of the Message Polynomial
        leading_term = integer_to_exponent[message[0]]
        multiplied_generator = exp_to_int([(term + leading_term) % 255 for term in generator])

        # XOR the result with the message polynomial
        for index, generator_term in enumerate(multiplied_generator):
            message[index] ^= generator_term

        if message[0] == 0:
            message.pop(0)     

    return message

n_groups = 1 if len(error_correction_information) == 4 else 2
codewords_index = 0
error_correction_codewords_per_block = error_correction_information[1]

DATA_CODEWORDS = [BIT_STRING[i:i+8] for i in range(0, len(BIT_STRING), 8)]
print(error_correction_codewords_per_block)
DATA_CODEWORDS_GROUPS = []

for group in range(n_groups):
    # obtain group specs
    blocks_in_group = error_correction_information[2 + 2 * group]
    codewords_per_block = error_correction_information[3 + 2 * group]
    
    GROUP = []

    for block in range(blocks_in_group):
        # Obtain the message polynomial from CODEWORDS
        message_polynomial_binary = [DATA_CODEWORDS[codewords_index + cw] for cw in range(codewords_per_block)]
        codewords_index += codewords_per_block

        # Turn message_polynomial_binary to integers
        message_polynomial = [int(bite,2) for bite in message_polynomial_binary]

        # Add block to group
        GROUP.append(message_polynomial)


    DATA_CODEWORDS_GROUPS.append(GROUP)

ERROR_CORRECTION_CODEWORD_GROUPS = []
generator_polynomial = generate_generator_polynomial(error_correction_codewords_per_block)

for data_group in DATA_CODEWORDS_GROUPS:
    GROUP = []

    for message_polynomial in data_group:      
        # Calculate the polynomial long devision of message_polynomial and generator_polynomial
        long_devision_result = polynomial_long_devision(message_polynomial, generator_polynomial)

        # Add block to group
        GROUP.append(long_devision_result)

    ERROR_CORRECTION_CODEWORD_GROUPS.append(GROUP)

#endregion

#region --- STEP 4 --- Strtucture Final Message

def zip_array(array: list[list]):
    zipped_array = []
    max_length = max([len(a) for a in array])
    for index in range(max_length):
        for list in array:
            if len(list) <= index:
                continue
            zipped_array.append(list[index])
    return zipped_array

def list_join(array: list[list]):
    new_array = []
    for list in array:
        new_array += list
    return new_array

DATA_CODEWORD_BLOCKS = list_join(DATA_CODEWORDS_GROUPS)
ERROR_CORRECTION_CODEWORD_BLOCKS = list_join(ERROR_CORRECTION_CODEWORD_GROUPS)
print("".join([bin(a)[2:].zfill(8) for a in list_join(ERROR_CORRECTION_CODEWORD_BLOCKS)]))

DATA_CODEWORDS_ZIPPED = zip_array(DATA_CODEWORD_BLOCKS)
ERROR_CORRECTION_CODEWORDS_ZIPPED = zip_array(ERROR_CORRECTION_CODEWORD_BLOCKS)

MESSAGE_CODEWORDS = DATA_CODEWORDS_ZIPPED + ERROR_CORRECTION_CODEWORDS_ZIPPED

leading_zeros_count = 0 if QR_CODE_VERSION == 1 else (4 - (floor(QR_CODE_VERSION / 7 - 3) ** 2)) % 12
print(leading_zeros_count)
MESSAGE = "".join([bin(codeword)[2:].zfill(8) for codeword in MESSAGE_CODEWORDS]) + "0" * leading_zeros_count

#endregion
print(MESSAGE)

#region --- STEP 5 --- Module Placement in Matrix

VAR_QR_SIZE = QR_CODE_VERSION * 4 + 17

QR_CODE = Image.new(mode="RGB", size=(VAR_QR_SIZE, VAR_QR_SIZE), color=(255,255,255))

white = (255, 255, 255)
black = (0, 0, 0)

color_finder_pattern = (255, 0, 0)
color_aligntment_pattern = (0, 255, 0)
color_timing_pattern = (0, 0, 255)
color_single_pixel = (255, 174, 0)
color_format_information = (255, 255, 0)

all_black = True
if all_black:
    color_finder_pattern = black
    color_aligntment_pattern = black
    color_timing_pattern = black
    color_single_pixel = black
    color_format_information = black


alignment_pattern_coordinates = {
    1: [],
    2: [6, 18],
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98, 122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170]
}

# Finder Pattern
#   Top Left
QR_CODE.paste(color_finder_pattern, (0,0,7,7))
QR_CODE.paste(white, (1,1,6,6))
QR_CODE.paste(color_finder_pattern, (2,2,5,5))
#   Top Right
QR_CODE.paste(color_finder_pattern, (VAR_QR_SIZE - 7,0,VAR_QR_SIZE,7))
QR_CODE.paste(white, (VAR_QR_SIZE - 6,1,VAR_QR_SIZE - 1,6))
QR_CODE.paste(color_finder_pattern, (VAR_QR_SIZE - 5,2,VAR_QR_SIZE - 2,5))
#   Bottom Right
QR_CODE.paste(color_finder_pattern, (0,VAR_QR_SIZE - 7,7,VAR_QR_SIZE))
QR_CODE.paste(white, (1,VAR_QR_SIZE - 6,6,VAR_QR_SIZE - 1))
QR_CODE.paste(color_finder_pattern, (2,VAR_QR_SIZE - 5,5,VAR_QR_SIZE - 2))


# Timing Pattern
for x in range(8, VAR_QR_SIZE - 7):
    QR_CODE.putpixel((x,6), white if x%2 else color_timing_pattern)

for y  in range(8, VAR_QR_SIZE - 7):
    QR_CODE.putpixel((6,y), white if y%2 else color_timing_pattern)

QR_CODE.putpixel((8, VAR_QR_SIZE - 8), color_single_pixel)

# Alignment Patterns
alignment_pattern_coords = alignment_pattern_coordinates[QR_CODE_VERSION]

for x_index, x in enumerate(alignment_pattern_coords):
    for y_index, y in enumerate(alignment_pattern_coords):
        if (x_index == 0 or x_index == len(alignment_pattern_coords) - 1) and (y_index == 0 or y_index == len(alignment_pattern_coords) - 1) and not (x_index == len(alignment_pattern_coords) - 1 and y_index == len(alignment_pattern_coords) - 1):
            continue
        QR_CODE.paste(color_aligntment_pattern, (x-2,y-2,x+3,y+3))
        QR_CODE.paste(white, (x-1,y-1,x+2,y+2))
        QR_CODE.putpixel((x,y), color_aligntment_pattern)

def max_step_dist(A, B):
    return max(abs(A[0] - B[0]), abs(A[1] - B[1]))

def is_data_or_ec(x, y):
    # Timing Patterns
    if x == 6 or y == 6:
        return False

    # Finder Patterns & Format Information Area
    dist_to_corners = [max_step_dist([x, y], corner) for corner in [[1, 1], [VAR_QR_SIZE-1, 1], [1, VAR_QR_SIZE-1]]]
    if min(dist_to_corners) <= 7:
        return False

    # Alignment Patterns
    for x_index, X in enumerate(alignment_pattern_coords):
        for y_index, Y in enumerate(alignment_pattern_coords):
            if (x_index == 0 or x_index == len(alignment_pattern_coords) - 1) and (y_index == 0 or y_index == len(alignment_pattern_coords) - 1) and not (x_index == len(alignment_pattern_coords) - 1 and y_index == len(alignment_pattern_coords) - 1):
                        continue
            if max_step_dist([x, y], [X, Y]) <= 2:
                return False

    # Version Information Area
    if QR_CODE_VERSION < 7:
        return True

    dist_to_corners = [max_step_dist([x, y], corner) for corner in [[0, VAR_QR_SIZE-6], [VAR_QR_SIZE-6, 0]]]
    if min(dist_to_corners) <= 5:
        return False

    return True

MESSAGE_TODO = [(bit == '1') for bit in MESSAGE]
print(len(MESSAGE_TODO))
print(["".join(MESSAGE[i:i+8]) for i in range(0, len(MESSAGE), 8)])
def place(x, y):   
    QR_CODE.putpixel((x,y), white if MESSAGE_TODO.pop(0) else black)

def fill_step_up(X, Y):
    for i in range(2):
        dx = -(i%2)

        x = X+dx
        y = Y

        if not is_data_or_ec(x,y):
            continue

        place(x, y)
        
def fill_step_down(X, Y):
    for i in range(2):
        dx = -(i%2)
        x = X+dx
        y = Y

        if not is_data_or_ec(x,y):
            continue

        place(x, y)

def fill_column_up(X):
    for Y in reversed(range(0, VAR_QR_SIZE)):
        fill_step_up(X, Y)

def fill_column_down(X):
    for Y in range(0, VAR_QR_SIZE):
        fill_step_down(X, Y)

X = VAR_QR_SIZE - 1
going_up = True

while X > 0:
    if going_up:
        fill_column_up(X)
    else:
        fill_column_down(X)

    going_up = not going_up
    X -= 2

    if X == 6:
        X -= 1

print(f"left: {MESSAGE_TODO}")
#endregion


#region --- STEP 6 --- Data Masking

# Mask
def mask(i, x, y):
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
            return not ((np.floor(x/3) + np.floor(y/3)) % 2)
        case 5:
            return not ((x * y) % 2 + (x * y) % 3)
        case 6:
            return not (((x * y) % 2 + (x * y) % 3) % 2)
        case 7:
            return not (((x + y) % 2 + (x * y) % 3) % 2)


def mask_bit(x, y, mask_pattern):
    bit = 0 if QR_CODE.getpixel((x,y)) == white else 1
    if is_data_or_ec(x,y) and mask(mask_pattern, x, y):
        return 1-bit
    return bit

def sign(x):
    return 1 if x>0 else -1

evaluation_1 = [0 for _ in range(8)]
evaluation_2 = [0 for _ in range(8)]
evaluation_3 = [0 for _ in range(8)]
evaluation_4 = []
same_counter = [-1 for _ in range(8)]
black_counter = [1 for _ in range(8)]

pattern = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]

# for mask_pattern in range(8):
#     for y in range(VAR_QR_SIZE):

#         same_counter[mask_pattern] = sign(mask_bit(0, y, mask_pattern))
        
#         for x in range(VAR_QR_SIZE):
#             bit = mask_bit(x, y, mask_pattern)

#             # Evaluation 1
#             if x > 0:
#                 if sign(bit) == sign(same_counter[mask_pattern]):
#                     same_counter[mask_pattern] += sign(bit)
#                 else:
#                     if abs(same_counter[mask_pattern]) >= 5:
#                         evaluation_1[mask_pattern] += abs(same_counter[mask_pattern]) - 2
#                     same_counter[mask_pattern] = sign(bit)

#             # Evaluation 2
#             if x>0 and y>0:
#                 bits = [
#                     mask_bit(x-1,y-1,mask_pattern),
#                     mask_bit(x,y-1,mask_pattern),
#                     mask_bit(x-1,y,mask_pattern),
#                 ]
#                 if bits.count(bit) == 3:
#                     evaluation_2[mask_pattern] += 3

#             # Evaluation 3
#             if x >= 10:
#                 is_pattern_1 = True
#                 is_pattern_2 = True
#                 for i in range(11):
#                     X = x - 10 + i
#                     if mask_bit(X, y, mask_pattern) != pattern[i]:
#                         is_pattern_1 = False
#                     else:
#                         is_pattern_2 = False
#                 if is_pattern_1 or is_pattern_2:
#                     evaluation_3[mask_pattern] += 40
#             if y >= 10:
#                 is_pattern_1 = True
#                 is_pattern_2 = True
#                 for i in range(11):
#                     Y = y - 10 + i
#                     if mask_bit(x, Y, mask_pattern) != pattern[i]:
#                         is_pattern_1 = False
#                     if mask_bit(x, Y, mask_pattern) != pattern[10-i]:
#                         is_pattern_2 = False
#                 if is_pattern_1 or is_pattern_2:
#                     evaluation_3[mask_pattern] += 40

#             # Evaluation 4
#             if bit == 0:
#                 black_counter[mask_pattern] += 1

# same_counter = [0 for _ in range(8)]

# # Evaluation 1 vertical
# for mask_pattern in range(8):
#     for x in range(VAR_QR_SIZE):
#         same_counter[mask_pattern] = sign(mask_bit(x, 0, mask_pattern))
#         for y in range(1, VAR_QR_SIZE):
#             bit = mask_bit(x, y, mask_pattern)

#             if sign(bit) == sign(same_counter[mask_pattern]):
#                 same_counter[mask_pattern] += sign(bit)
#             else:
#                 if abs(same_counter[mask_pattern]) >= 5:
#                     evaluation_1[mask_pattern] += abs(same_counter[mask_pattern]) - 2
#                 same_counter[mask_pattern] = sign(bit)

# # Evaluation 4
# n_pixels = VAR_QR_SIZE ** 2
# for count in black_counter:
#     percentile = (count / n_pixels) * 100

#     lower = int(abs(floor(percentile / 5) * 5 - 50) / 5)
#     upper = int(abs(ceil(percentile / 5) * 5 - 50) / 5)

#     evaluation_4.append(min(lower, upper))

# # Combine evaluations
# evaluations = []
# for i in range(8):
#     evaluations.append(evaluation_1[i] + evaluation_2[i] + evaluation_3[i] + evaluation_4[i])

def apply_mask(mask_pattern):
    for x in range(VAR_QR_SIZE):
        for y in range(VAR_QR_SIZE):
            if is_data_or_ec(x, y):
                QR_CODE.putpixel((x,y), black if mask_bit(x, y, mask_pattern) == 0 else white)

# if not FORCE_FORMAT:
#     MASK_PATTERN = evaluations.index(min(evaluations))
# print(evaluation_1)
# print(evaluation_2)
# print(evaluation_3)
# print(evaluation_4)
# print(evaluations)
print(f"MASK_PATTERN: {MASK_PATTERN}")
apply_mask(MASK_PATTERN)
print(VAR_QR_SIZE)

#endregion


#region --- STEP 7 --- Format and Version Information

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

# Format Information
def format_string(ERROR_CORRECTION_LEVEL, MASK_PATTERN):
    format_error_correction_binary ={
        'L': 0b01,
        'M': 0b00,
        'Q': 0b11,
        'H': 0b10
    }

    generator = 0b10100110111
    format_information_mask = 0b101010000010010

    format_information = (format_error_correction_binary[ERROR_CORRECTION_LEVEL] << 3) | MASK_PATTERN

    format_information_error_correction = format_information << 10

    while format_information_error_correction >= (1<<10):
        padded_generator = generator << (floor(np.log2(format_information_error_correction)) - 10)
        format_information_error_correction ^= padded_generator

    format_information_encoded = (format_information << 10) | format_information_error_correction
    format_information_encoded ^= format_information_mask

    return bin(format_information_encoded)[2:].zfill(15)

format_information_encoded = format_string(ERROR_CORRECTION_LEVEL, MASK_PATTERN)

for i in range(15):
    a, b = format_information_coordinates[i]
    QR_CODE.putpixel(b, color_format_information if format_information_encoded[i] == "1" else white)
    QR_CODE.putpixel(a, color_format_information if format_information_encoded[i] == "1" else white)

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

if QR_CODE_VERSION >= 7:
    version_information_string = version_information_string_dict[QR_CODE_VERSION]

    bottom_start_x = 0
    bottom_start_y = VAR_QR_SIZE - 11

    for dx in range(6):
        for dy in range(3):
            index = 17 - dx * 3 - dy
            QR_CODE.putpixel((bottom_start_x + dx, bottom_start_y + dy), color_format_information if version_information_string[index] == '1' else white)

    right_start_x = VAR_QR_SIZE - 11
    right_start_y = 0

    for dy in range(6):
        for dx in range(3):
            index = 17 - dy * 3 - dx
            QR_CODE.putpixel((right_start_x + dx, right_start_y + dy), color_format_information if version_information_string[index] == '1' else white)


#endregion


#region --- STEP 8 --- Display

# Display
PADDED_QR_CODE = Image.new(QR_CODE.mode, (VAR_QR_SIZE + 8, VAR_QR_SIZE + 8), white)
PADDED_QR_CODE.paste(QR_CODE, (4, 4))
SCALED_QR_CODE = PADDED_QR_CODE.resize(((VAR_QR_SIZE + 8) * DEV_VIEW_SCALE_FACTOR, (VAR_QR_SIZE + 8) * DEV_VIEW_SCALE_FACTOR), resample=Image.Resampling.NEAREST)
PADDED_QR_CODE.save("qr_code.png")
SCALED_QR_CODE.show()

# ALL_MASKS = Image.new(QR_CODE.mode, (4*(VAR_QR_SIZE + 4) + 4, 2*(VAR_QR_SIZE + 4) + 4), white)
# for y in range(2):
#     for x in range(4):
#         apply_mask(x+4*y)
#         ALL_MASKS.paste(QR_CODE, (4+x*(VAR_QR_SIZE + 4), 4+y*(VAR_QR_SIZE + 4)))
#         apply_mask(x+4*y)

# ALL_MASKS.show()
#endregion

