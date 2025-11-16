from io_device import Io

class Memory:
    def __init__(self):
        # ============================
        # MAPEAMENTO DE MEMÓRIA
        # ============================

        # RAM: 0x00000 – 0x7FFFF (512 KB)
        self.RAM_BASE = 0x00000
        self.RAM_SIZE = 0x80000
        self.ram = [0] * self.RAM_SIZE

        # VRAM: 0x80000 – 0x8FFFF (64 KB)
        self.VRAM_BASE = 0x80000
        self.VRAM_SIZE = 0x10000
        self.vram = [0] * self.VRAM_SIZE

        # I/O: 0x9FC00 – 0x9FFFF (1 KB)
        self.IO_BASE = 0x9FC00
        self.IO_SIZE = 0x400
        self.io = Io()

    def decode(self, addr):
        if 0 <= addr < self.RAM_SIZE:
            return ("ram", addr)

        elif self.VRAM_BASE <= addr < self.VRAM_BASE + self.VRAM_SIZE:
            return ("vram", addr - self.VRAM_BASE)

        elif self.IO_BASE <= addr < self.IO_BASE + self.IO_SIZE:
            return ("io", addr)

        else:
            return ("reserved", None)

    def read8(self, addr):
        region, offset = self.decode(addr)

        if region == "ram": return self.ram[offset]
        if region == "vram": return self.vram[offset]
        if region == "io": return self.io.read(addr)

        print(f"[WARN] read8 em região reservada 0x{addr:08X}")
        return 0

    def read16(self, addr):
        b0 = self.read8(addr)
        b1 = self.read8(addr + 1)
        return b0 | (b1 << 8)

    def read32(self, addr):
        b0 = self.read8(addr)
        b1 = self.read8(addr + 1)
        b2 = self.read8(addr + 2)
        b3 = self.read8(addr + 3)
        return b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)

    def write8(self, addr, value):
        region, offset = self.decode(addr)

        value &= 0xFF

        if region == "ram":
            self.ram[offset] = value
            return

        if region == "vram":
            self.vram[offset] = value
            return

        if region == "io":
            self.io.write(addr, value)
            return

        print(f"[WARN] write8 em região reservada 0x{addr:08X}")

    def write16(self, addr, value):
        self.write8(addr, value & 0xFF)
        self.write8(addr + 1, (value >> 8) & 0xFF)

    def write32(self, addr, value):
        self.write8(addr, value & 0xFF)
        self.write8(addr + 1, (value >> 8) & 0xFF)
        self.write8(addr + 2, (value >> 16) & 0xFF)
        self.write8(addr + 3, (value >> 24) & 0xFF)

    