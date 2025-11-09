class Io:
    def __init__(self):
        # vamos simular uma pequena área de vídeo (VRAM)
        self.vram_start = 0x80000
        self.vram_end = 0x8FFFF
        self.vram = [0] * (self.vram_end - self.vram_start + 1)

    def write(self, address: int, value: int):
        """Escreve na área de IO (por enquanto, só VRAM e terminal)"""
        if self.vram_start <= address <= self.vram_end:
            self.vram[address - self.vram_start] = value & 0xFF
        elif address == 0x9FC00:
            # escreve caractere no terminal (simula saída)
            print(chr(value & 0xFF), end='')

    def read(self, address: int):
        """Lê valor da área de IO"""
        if self.vram_start <= address <= self.vram_end:
            return self.vram[address - self.vram_start]
        return 0
