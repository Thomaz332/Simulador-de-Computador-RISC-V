from memory import Memory
from io_device import Io
from bus import Bus
from cpu import CPU

# Inicialização dos dispositivos
mem = Memory()
io = Io()
bus = Bus(mem, io)
cpu = CPU(bus)

# ============================
# Programa de teste: 
# Escrever "HELLO WORLD\n" na VRAM
# usando instruções RISC-V
# ============================

# Endereço base da VRAM
VRAM_BASE = 0x80000

# String que vamos escrever
msg = b"HELLO WORLD\n"

# Gerar um pequeno programa RISC-V:
# t0 = VRAM_BASE
# t1 = msg[i]
# sb t1, i(t0)

# Registradores:
# t0 = x5
# t1 = x6

# --- Carregar endereço base da VRAM em t0 (x5) ---
# LUI x5, upper(80000)
upper = (VRAM_BASE >> 12) & 0xFFFFF
mem.write32(0,  (upper << 12) | (5 << 7) | 0x37)  # LUI x5, upper

# --- Escrever cada caractere ---
pc = 4
for i, b in enumerate(msg):
    # ADDI x6, x0, b      (t1 = caractere)
    instr_addi = (b << 20) | (0 << 15) | (6 << 7) | (0x13)
    mem.write32(pc, instr_addi)
    pc += 4

    # SB x6, i(x5)
    imm11_5 = (i >> 5) & 0x7F
    imm4_0  = i & 0x1F
    instr_sb = (imm11_5 << 25) | (6 << 20) | (5 << 15) | (0x0 << 12) | (imm4_0 << 7) | 0x23
    mem.write32(pc, instr_sb)
    pc += 4

# Loop infinito para não sair do programa
# JAL x0, 0
mem.write32(pc, 0x0000006F)


# ============================
# EXECUÇÃO DO CPU
# ============================

print("Executando...\n")

# Rode bastante instruções — o dump aparecerá automático
for _ in range(50):
    cpu.step()

"""
# TESTE DAS OPERAÇÕES

cpu.regs[1] = 10       # x1 = 10
cpu.regs[2] = 20       # x2 = 20

# R-type
mem.write32(0,  0x002081B3)  # ADD 
mem.write32(4,  0x40208233)  # SUB
mem.write32(8,  0x0020F2B3)  # AND
mem.write32(12, 0x0020E333)  # OR
mem.write32(16, 0x0020C3B3)  # XOR

# SHIFTs
mem.write32(20, 0x002093B3)  # SLL
mem.write32(24, 0x0020D433)  # SRL
mem.write32(28, 0x4020D4B3)  # SRA

# SLT / SLTU
mem.write32(32, 0x0020A533)  # SLT
mem.write32(36, 0x0020B5B3)  # SLTU

# I-Type
mem.write32(40, 0x00A0C613)  # XORI
mem.write32(44, 0x00A0E693)  # ORI
mem.write32(48, 0x00A0F713)  # ANDI

# LOAD e STORE
mem.write32(52, 0x0050A023)  # SW
mem.write32(56, 0x0000A283)  # LW 

# Executa as instruções
for _ in range(15):
    cpu.step()

# Resultado

print("\n=== RESULTADOS ===")
print(f"x3  (ADD)   = {cpu.regs[3]}")
print(f"x4  (SUB)   = {cpu.regs[4]}")
print(f"x5  (AND)   = {cpu.regs[5]}")
print(f"x6  (OR)    = {cpu.regs[6]}")
print(f"x7  (XOR)   = {cpu.regs[7]}")
print(f"x8  (SLL)   = {cpu.regs[8]}")
print(f"x9  (SRL)   = {cpu.regs[9]}")
print(f"x10 (SRA)   = {cpu.regs[10]}")
print(f"x11 (SLT)   = {cpu.regs[11]}")
print(f"x12 (SLTU)  = {cpu.regs[12]}")
print(f"x13 (XORI)  = {cpu.regs[13]}")
print(f"x14 (ORI)   = {cpu.regs[14]}")
print(f"x15 (ANDI)  = {cpu.regs[15]}")
print(f"x5 LOAD     = {cpu.regs[5]}  (após SW/LW)")
"""

# """