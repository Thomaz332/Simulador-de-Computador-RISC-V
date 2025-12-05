class Io:
    def write(self, address: int, value: int):
        # Terminal
        if address == 0x9FC00:
            print(chr(value & 0xFF), end="")
            return

    def read(self, address: int):
        
        return 0


    
