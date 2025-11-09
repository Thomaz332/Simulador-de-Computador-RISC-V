from memory import Memory
from io_device import Io

class Bus:
    def __init__(self, memory: Memory, io_dev: Io):
        self.memory = memory
        self.io = io_dev

    def read(self, address: int):
        """Lê da memória ou IO dependendo do endereço"""
        #endereço < 0x80000	= Memória RAM	
        #endereço ≥ 0x80000	= IO (entrada/saída)
        if address >= 0x80000:
            return self.io.read(address)
        else:
            return self.memory.read32(address)

    def write(self, address: int, value: int):
        """Escreve na memória ou IO dependendo do endereço"""
        #endereço < 0x80000	= Memória RAM	
        #endereço ≥ 0x80000	= IO (entrada/saída)
        if address >= 0x80000:
            self.io.write(address, value)
        else:
            self.memory.write32(address, value)
