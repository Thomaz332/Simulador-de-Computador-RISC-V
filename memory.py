class Memory:
    def __init__(self, matrizMemoria,size: int):       
            self.matrizMemoria = matrizMemoria[32]

            # RAM Principal
            for endereco in range(0x00000, 0x80000):
                self.matrizMemoria[f"0x{endereco:05X}"] = "RAM Principal (Programa, Dados, Pilha, Heap)"

            # VRAM
            for endereco in range(0x80000, 0x90000):
                self.matrizMemoria[f"0x{endereco:05X}"] = "VRAM (Vídeo RAM)"

            # Área Reservada
            for endereco in range(0x90000, 0x9FC00):
                self.matrizMemoria[f"0x{endereco:05X}"] = "Área Reservada para Expansão Futura"

            # Periféricos
            for endereco in range(0x9FC00, 0xA0000):
                self.matrizMemoria[f"0x{endereco:05X}"] = "Periféricos de Hardware (E/S Mapeada)"

            self.data = [0] * size
    
    #Le um byte
    def read8(self, address: int) -> int:
        if address < 0 or address >= len(self.data):
            raise IndexError("Read8: endereço fora da memória")
        return self.data[address]

    #Le 4 byte
    def read32(self, address: int) -> int:
        if address + 3 >= len(self.data):
            raise IndexError("Read32: endereço fora da memória")

        # junta os 4 bytes little-endian
        return (
            self.data[address]
            | (self.data[address + 1] << 8)
            | (self.data[address + 2] << 16)
            | (self.data[address + 3] << 24)
        )

    def write8(self, address: int, value: int):
        if address < 0 or address >= len(self.data):
            raise IndexError("Write8: endereço fora da memória")
        self.data[address] = value & 0xFF  # garante 8 bits

    def write32(self, address: int, value: int):
        if address + 3 >= len(self.data):
            raise IndexError("Write32: endereço fora da memória")

        self.data[address] = value & 0xFF
        self.data[address + 1] = (value >> 8) & 0xFF
        self.data[address + 2] = (value >> 16) & 0xFF
        self.data[address + 3] = (value >> 24) & 0xFF

    def get_size(self) -> int:
        return len(self.data)
