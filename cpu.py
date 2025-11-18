from bus import Bus

def to_u32(x):
        return x & 0xFFFFFFFF
    
def to_s32(x):
    x = x & 0xFFFFFFFF
    return x if x < 0x80000000 else x - 0x100000000

class CPU:
    def __init__(self, bus: Bus):
        self.bus = bus
        self.regs = [0] * 32
        self.pc = 0
        self.instr_count = 0

    def reset(self):
        self.regs = [0] * 32
        self.pc = 0

    def fetch(self):
        instr = self.bus.read(self.pc)
        return instr

    def step(self):
        instr = self.fetch()
        self.decode_and_execute(instr)
        self.regs[0] = 0 # x0 sempre zero

        self.instr_count += 1

        if self.instr_count == 50:
            self.dump_vram_to_terminal()

    # =================================================================
    # DECODIFICAÇÃO COMPLETA RV32I
    # =================================================================
    def decode_and_execute(self, instr):

        opcode = instr & 0x7F
        rd     = (instr >> 7)  & 0x1F
        funct3 = (instr >> 12) & 0x7
        rs1    = (instr >> 15) & 0x1F
        rs2    = (instr >> 20) & 0x1F
        funct7 = (instr >> 25)

        pc_next = to_u32(self.pc + 4)
        imm_i = (instr >> 20) & 0xFFF
        if imm_i & 0x800:
            imm_i -= 0x1000

        # ================================================================
        # LUI
        # ================================================================
        if opcode == 0x37:
            imm_u = instr & 0xFFFFF000
            self.regs[rd] = to_u32(imm_u)
            self.pc = pc_next
            return

        # ================================================================
        # AUIPC
        # ================================================================
        if opcode == 0x17:
            imm_u = instr & 0xFFFFF000
            self.regs[rd] = to_u32(self.pc + imm_u)
            self.pc = pc_next
            return

        # ================================================================
        # JAL
        # ================================================================
        if opcode == 0x6F:
            imm = (
                ((instr >> 31) & 1) << 20 |
                ((instr >> 21) & 0x3FF) << 1 |
                ((instr >> 20) & 1) << 11 |
                ((instr >> 12) & 0xFF) << 12    
            )

            # Sign extend 21 bits   
            if imm & (1 << 20):
                imm -= (1 << 21)

            self.regs[rd] = pc_next
            self.pc = (self.pc + imm) & 0xFFFFFFFF
            return

        # ================================================================
        # JALR
        # ================================================================
        if opcode == 0x67:
            self.regs[rd] = pc_next
            target = to_u32(self.regs[rs1] + imm_i) & ~1
            self.pc = target
            return

        # ================================================================
        # BRANCHES (BEQ, BNE, BLT, BGE, BLTU, BGEU)
        # ================================================================
        if opcode == 0x63:
            # Monta imediato B-type (signed)
            imm = (
                  ((instr >> 31) & 0x1) << 12 |
                  ((instr >> 7)  & 0x1) << 11 |
                  ((instr >> 25) & 0x3F) << 5 |
                  ((instr >> 8)  & 0xF) << 1
            )

            if imm & (1 << 12):
                imm |= ~((1 << 13) - 1)

            x = self.regs[rs1]
            y = self.regs[rs2]
            xu = self.regs[rs1] & 0xFFFFFFFF
            yu = self.regs[rs2] & 0xFFFFFFFF

            take = False
            if   funct3 == 0x0: take = (x == y)              # BEQ (signed/non depende)
            elif funct3 == 0x1: take = (x != y)              # BNE
            elif funct3 == 0x4: take = (x < y)               # BLT (signed)
            elif funct3 == 0x5: take = (x >= y)              # BGE (signed)
            elif funct3 == 0x6: take = (xu < yu)             # BLTU (unsigned)
            elif funct3 == 0x7: take = (xu >= yu)            # BGEU (unsigned)

            self.pc = (self.pc + imm) if take else pc_next
            return

        # ================================================================
        # LOADS (LB, LH, LW, LBU, LHU)
        # ================================================================
        if opcode == 0x03:
            addr = to_u32(self.regs[rs1] + imm_i)

            if funct3 == 0x0: # LB
                v = self.bus.read8(addr)
                if v & 0x80: v |= 0xFFFFFF00
            elif funct3 == 0x1: # LH
                v = self.bus.read16(addr)
                if v & 0x8000: v |= 0xFFFF0000
            elif funct3 == 0x2: # LW
                v = self.bus.read(addr)
            elif funct3 == 0x4: # LBU
                v = self.bus.read8(addr)
            elif funct3 == 0x5: # LHU
                v = self.bus.read16(addr)
            else:
                v = 0
                print(f"[WARN] LOAD funct3={funct3}")

            self.regs[rd] = v & 0xFFFFFFFF
            pc_next = to_u32(self.pc + 4)
            return

        # ================================================================
        # STORES (SB, SH, SW)
        # ================================================================
        if opcode == 0x23:
            imm = ((instr >> 7) & 0x1F) | ((instr >> 25) << 5)
            if imm & 0x800:
                imm |= 0xFFFFF000
            imm &= 0xFFFFFFFF

            addr = to_u32(self.regs[rs1] + to_s32(imm))
            val  = to_u32(self.regs[rs2])

            if   funct3 == 0x0: self.bus.write8(addr, val)
            elif funct3 == 0x1: self.bus.write16(addr, val)
            elif funct3 == 0x2: self.bus.write(addr, val)
            else: print(f"[WARN] STORE funct3={funct3}")

            pc_next = to_u32(self.pc + 4)
            return

        # ================================================================
        # I-TYPE ALU (ADDI, SLTI, SLTIU, XORI, ORI, ANDI)
        # ================================================================
        if opcode == 0x13:

            if funct3 == 0x0: # ADDI
                self.regs[rd] = (self.regs[rs1] + imm_i) & 0xFFFFFFFF

            elif funct3 == 0x2: # SLTI
                self.regs[rd] = 1 if int(self.regs[rs1]) < int(imm_i) else 0

            elif funct3 == 0x3: # SLTIU
                self.regs[rd] = 1 if (self.regs[rs1] & 0xFFFFFFFF) < (imm_i & 0xFFFFFFFF) else 0

            elif funct3 == 0x4: # XORI
                self.regs[rd] = self.regs[rs1] ^ imm_i

            elif funct3 == 0x6: # ORI
                self.regs[rd] = self.regs[rs1] | imm_i

            elif funct3 == 0x7: # ANDI
                self.regs[rd] = self.regs[rs1] & imm_i

            elif funct3 == 0x1: # SLLI
                sh = (instr >> 20) & 0x1F # shamt = bits 20–24
                self.regs[rd] = (self.regs[rs1] << sh) & 0xFFFFFFFF

            elif funct3 == 0x5:
                sh = (instr >> 20) & 0x1F # shamt = bits 20–24
                if funct7 == 0x00: # SRLI
                    self.regs[rd] = (self.regs[rs1] >> sh) & 0xFFFFFFFF
                else: # SRAI
                    self.regs[rd] = (int(self.regs[rs1]) >> sh) & 0xFFFFFFFF # aritmético: preservar sinal

            pc_next = to_u32(self.pc + 4)
            return

        # ================================================================
        # R-TYPE (ADD, SUB, SLL, SLT, SLTU, XOR, SRL, SRA, OR, AND)
        # ================================================================
        if opcode == 0x33:
            a = self.regs[rs1]
            b = self.regs[rs2]

            if funct3 == 0x0: 
                if funct7 == 0x00: self.regs[rd] = (a + b) & 0xFFFFFFFF 
                else:              self.regs[rd] = (a - b) & 0xFFFFFFFF 
            elif funct3 == 0x1: self.regs[rd] = (a << (b & 0x1F)) & 0xFFFFFFFF 
            elif funct3 == 0x2: self.regs[rd] = 1 if int(a) < int(b) else 0 
            elif funct3 == 0x3: self.regs[rd] = 1 if (a & 0xFFFFFFFF) < (b & 0xFFFFFFFF) else 0 
            elif funct3 == 0x4: self.regs[rd] = a ^ b 
            elif funct3 == 0x5: 
                if funct7 == 0x00: self.regs[rd] = (a >> (b & 0x1F)) & 0xFFFFFFFF
                else:              self.regs[rd] = (int(a) >> (b & 0x1F)) & 0xFFFFFFFF
            elif funct3 == 0x6: self.regs[rd] = a | b
            elif funct3 == 0x7: self.regs[rd] = a & b

            pc_next = to_u32(self.pc + 4)
            return

        print(f"[WARN] Instrução desconhecida 0x{instr:08X}")
        
    def dump_vram_to_terminal(self):
        print("\n--- VRAM DUMP ---")

        start = self.bus.io.VRAM_START
        end   = self.bus.io.VRAM_END

        for addr in range(start, end + 1):
            byte = self.bus.read8(addr)
            
            print(chr(byte), end="")

        print("\n--- END VRAM ---\n")
