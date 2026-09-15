
def create_byte(value:int, byte_size:int=8) -> str:
    return bin(value)[2:].zfill(byte_size)

def zip_array(array: list[list]):
    zipped_array = []
    max_length = max([len(a) for a in array])
    for index in range(max_length):
        for list in array:
            if len(list) <= index:
                continue
            zipped_array.append(list[index])
    return zipped_array