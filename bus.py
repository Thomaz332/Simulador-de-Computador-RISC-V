from memory import Memory
from io_device import Io

class Bus:
    def __init__(self, memory: Memory, io: Io):
        self.memory = memory
        self.io = io

    def read(self, addr):
        return self.memory.read32(addr)

    def write(self, addr, value):
        self.memory.write32(addr, value)
    
    def write(self, addr, value):
        self.io.write(addr, value)

    def read8(self, addr):
        return self.memory.read8(addr)

    def read16(self, addr):
        return self.memory.read16(addr)

    def write8(self, addr, value):
        self.memory.write8(addr, value)

    def write16(self, addr, value):
        self.memory.write16(addr, value)