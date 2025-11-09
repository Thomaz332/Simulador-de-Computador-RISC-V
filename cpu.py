from bus import Bus

class CPU:
    def __init__(self, bus: Bus):
        self.bus = bus
        self.regs = [0] * 32   # 32 registradores x0–x31
        self.pc = 0

    def reset(self):
        """Reseta CPU e registradores"""
        self.regs = [0] * 32
        self.pc = 0
    
    
    def fetch(self):
        """Busca uma instrução de 32 bits da memória"""
        instr = self.bus.read(self.pc)
        self.pc += 4
        return instr
    
    def decode_and_execute(self, instr: int):
        opcode = instr & 0x7F             # bits [6:0]
        rd = (instr >> 7) & 0x1F          # bits [11:7]
        funct3 = (instr >> 12) & 0x7      # bits [14:12]
        rs1 = (instr >> 15) & 0x1F        # bits [19:15]
        rs2 = (instr >> 20) & 0x1F        # bits [24:20]
        funct7 = (instr >> 25) & 0x7F     # bits [31:25]
        imm = (instr >> 20) & 0xFFF       # usado em I-type

        # extensão de sinal do imediato
        if imm & 0x800:
            imm |= 0xFFFFF000

        # ========== I-TYPE ==========
        #usa um registrador e um número constante (imediato)
        if opcode == 0x13 and funct3 == 0x0:   # ADDI
            self.regs[rd] = (self.regs[rs1] + imm) & 0xFFFFFFFF
            print(f"ADDI x{rd}, x{rs1}, {imm} → x{rd}={self.regs[rd]}")

        # ========== R-TYPE ==========
        #Usa dois registradores de entrada e um de saída
        elif opcode == 0x33:
            if funct3 == 0x0 and funct7 == 0x00:
                # ADD
                self.regs[rd] = (self.regs[rs1] + self.regs[rs2]) & 0xFFFFFFFF
                print(f"ADD x{rd}, x{rs1}, x{rs2} → x{rd}={self.regs[rd]}")
            elif funct3 == 0x0 and funct7 == 0x20:
                # SUB
                self.regs[rd] = (self.regs[rs1] - self.regs[rs2]) & 0xFFFFFFFF
                print(f"SUB x{rd}, x{rs1}, x{rs2} → x{rd}={self.regs[rd]}")
            elif funct3 == 0x7:
                # AND
                self.regs[rd] = self.regs[rs1] & self.regs[rs2]
                print(f"AND x{rd}, x{rs1}, x{rs2} → x{rd}={self.regs[rd]}")
            elif funct3 == 0x6:
                # OR
                self.regs[rd] = self.regs[rs1] | self.regs[rs2]
                print(f"OR x{rd}, x{rs1}, x{rs2} → x{rd}={self.regs[rd]}")
            elif funct3 == 0x4:
                # XOR
                self.regs[rd] = self.regs[rs1] ^ self.regs[rs2]
                print(f"XOR x{rd}, x{rs1}, x{rs2} → x{rd}={self.regs[rd]}")
            else:
                print(f"[WARN] Instrução R-type desconhecida: funct3={funct3}, funct7={funct7}")

        else:
            print(f"[WARN] Instrução desconhecida 0x{instr:08X}")

        # registrador x0 é sempre 0
        self.regs[0] = 0

    def step(self):
        """Executa um ciclo completo"""
        instr = self.fetch()
        self.decode_and_execute(instr)

