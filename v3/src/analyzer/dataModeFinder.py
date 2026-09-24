from config.constants import alphanumeric_table

class DataTypeFinder:
    def __init__(self):
        ...
    
    def execute(self, data:str):
        if data.isnumeric():
            return 0 # Numeric Mode

        for char in data:
            if not char in alphanumeric_table:
                return 2 # Bit mode

        return 1 # Alphanumeric Mode