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
        imm_i = (instr >> 20) & 0xFFF       # usado em I-type

        # extensão de sinal do imediato
        if imm_i & 0x800:
            imm_i |= 0xFFFFF000
        imm_i = imm_i & 0xFFFFFFFF

        # ========== Load (I-type) ==========
        # opcode 0x03 -> loads (LW, LB, LBU etc.). Implementamos LW (funct3 == 0x2)
        if opcode == 0x03:
            if funct3 == 0x2: # LW
                addr = (self.regs[rs1] + imm_i) & 0xFFFFFFFF
                if addr % 4 != 0:
                    print(f"[WARN] LW em endereço não alinhado: 0x{addr:08X}")
                val = self.bus.read(addr)
                self.regs[rd] = val & 0xFFFFFFFF
                print(f"LW x{rd}, {imm_i}(x{rs1}) -> x{rd}={self.regs[rd]} (addr=0x{addr:08X})")
            else:
                print(f"[WARN] LOAD desconhecido funct3={funct3}")

        # ========== STORE (S-type) =========
        # opcode 0x23 -> stores (SW etc...)
        elif opcode == 0x23:
            # S-type immediate: bits [11:5] = instr[31:25], bits [4:0] = instr[11:7]
            imm_s = ((instr >> 7) & 0x1F) | ((instr >> 25) << 5)
            # extensão de sinal (12 bits)
            if imm_s & 0x800:
                imm_s |= 0xFFFFF000
            imm_s = imm_s & 0xFFFFFFFF

            if funct3 == 0x2: #SW
                addr = (self.regs[rs1] + imm_s) & 0xFFFFFFFF
                if addr % 4 != 0:
                    print(f"[WARN] SW em endereço não alinhado: 0x{addr:08X}")
                value = self.regs[rs2] & 0xFFFFFFFF
                self.bus.write(addr, value)
                print(f"SW x{rs2} ({value}) -> {imm_s}(x{rs1}) (addr=0x{addr:08X})")
            else:
                print(f"[WARN] STORE desconhecido funct3={funct3}")

        # ========== I-TYPE ==========
        #usa um registrador e um número constante (imediato)
        elif opcode == 0x13 and funct3 == 0x0:   # ADDI
            self.regs[rd] = (self.regs[rs1] + (imm_i & 0xFFFFFFFF)) & 0xFFFFFFFF
            print(f"ADDI x{rd}, x{rs1}, {imm_i} → x{rd}={self.regs[rd]}")

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

