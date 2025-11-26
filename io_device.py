class Io:
    def write(self, address: int, value: int):
        # Terminal
        if address == 0x9FC00:
            print(chr(value & 0xFF), end="")
            return

        # outros futuros: teclado, timer...
        print(f"[WARN] IO write desconhecido: {address:08X}")

    def read(self, address: int):
        
        return 0
