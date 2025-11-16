class Io:
    def __init__(self):
        # VRAM = 64 KB (0x80000–0x8FFFF)
        self.VRAM_START = 0x80000
        self.VRAM_END   = 0x8FFFF
        
        size = self.VRAM_END - self.VRAM_START + 1
        self.vram = [0] * size

    def write(self, address: int, value: int):
        # ---- VRAM ----
        if self.VRAM_START <= address <= self.VRAM_END:
            index = address - self.VRAM_START
            self.vram[index] = value & 0xFF
            return

        # ---- Terminal ----
        if address == 0x9FC00:
            print(chr(value & 0xFF), end="")
            return

        # ---- OUTROS FUTUROS ----
        # teclado, som, timer, etc.

    def read(self, address: int):
        # ---- VRAM ----
        if self.VRAM_START <= address <= self.VRAM_END:
            return self.vram[address - self.VRAM_START]

        # ---- OUTROS ----
        return 0
