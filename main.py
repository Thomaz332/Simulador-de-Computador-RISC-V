from memory import Memory
from io_device import Io
from bus import Bus
from cpu import CPU

mem = Memory(); 
io = Io(); 
bus = Bus(mem, io); 
cpu = CPU(bus)

cpu.regs[1] = 20
cpu.regs[2] = 10

# Print terminal
#msg = "HELLO WORLD!\n"

#for i, c in enumerate(msg):
#    bus.write8(0x80000 + i, ord(c))
#bus.write8(0x80000 + len(msg), 0) 
#for i in range(10):
#    cpu.step()

# ===============================
# R-TYPE
# ===============================

# ADD esperado 30
#mem.write32(0,  0x002081B3)
#cpu.step()
#print(f"x3  (ADD)   = {cpu.regs[3]}")

# SUB esperado 10
#mem.write32(0,0x40208233)  
#cpu.step()
#print(f"x4  (SUB)   = {cpu.regs[4]}")

# AND esperado 0
#mem.write32(0,0x0020F2B3)
#cpu.step()
#print(f"x5  (AND)   = {cpu.regs[5]}")

# OR esperado 30
#mem.write32(0, 0x0020E333)
#cpu.step()
#print(f"x6  (OR)    = {cpu.regs[6]}")

# XOR esperado 30
#mem.write32(0, 0x0020C3B3)
#cpu.step()
#print(f"x7  (XOR)   = {cpu.regs[7]}")

# SLT esperado 0
#mem.write32(0, 0x0020A533)
#cpu.step()
#print(f"x10 (SLT)   = {cpu.regs[10]}")

# SLTU esperado 0
#mem.write32(0, 0x0020B5B3) 
#cpu.step()
#print(f"x12 (SLTU)  = {cpu.regs[12]}") 


# ===============================
# I-TYPE (ALU)
# ===============================

# ADDI esperado 25
#mem.write32(0, 0x00508593)
#cpu.step()
#print(f"x11 (ADDI)  = {cpu.regs[11]}")

# ANDI esperado 4
#mem.write32(0, 0x0050F613)
#cpu.step()
#print(f"x12 (ANDI)  = {cpu.regs[12]}")

# SLTI esperado 0
#mem.write32(0, 0x00A0A593)
#cpu.step()
#print(f"x11 (SLTI)  = {cpu.regs[11]}")

# SLTIU esperado 0
#mem.write32(0, 0x00A0B593)
#cpu.step()
#print(f"x11 (SLTIU) = {cpu.regs[11]}")

# SLLI esperado X
#mem.write32(0, 0x00109193)
#cpu.step()
#print(f"x3  (SLLI)  = {cpu.regs[3]}")

# SRLI esperado X
#mem.write32(0, 0x0010D193)
#cpu.step()
#print(f"x3  (SRLI)  = {cpu.regs[3]}")

# SRAI esperado X
#mem.write32(0, 0x4010D193)
#cpu.step()
#print(f"x3  (SRAI)  = {cpu.regs[3]}")

# ===============================
# B-TYPE (BRANCHES)
# ===============================

# BEQ (não pula)
#mem.write32(0, 0x00208663)
#cpu.step()

# BNE (pula)
#mem.write32(0, 0x00209663)
#cpu.step()

# BLT (não pula)
#mem.write32(0, 0x0020C663)
#cpu.step()

# BGE (pula)
#mem.write32(0, 0x0020D663)
#cpu.step()

# BLTU (não pula)
#mem.write32(0, 0x0020E663)
#cpu.step()

# BGEU (pula)
#mem.write32(0, 0x0020F663)
#cpu.step()

# ===============================
# J-TYPE
# ===============================

# JAL esperado alterar PC
#mem.write32(0, 0x004000EF)
#cpu.step()
#print(f"x1  (JAL)   = {cpu.regs[1]}")

# JALR esperado alterar PC
#mem.write32(0, 0x000080E7)
#cpu.step()
#print(f"x1  (JALR)  = {cpu.regs[1]}")

# ===============================
# LOAD
# ===============================

# LB 
#mem.write32(0, 0x0000A083)
#cpu.step()
#print(f"x1  (LB)    = {cpu.regs[1]}")

# LH 
#mem.write32(0, 0x0000A103)
#cpu.step()
#print(f"x2  (LH)    = {cpu.regs[2]}")

# LW 
#mem.write32(0, 0x0000A183)
#cpu.step()
#print(f"x3  (LW)    = {cpu.regs[3]}")

# LBU 
#mem.write32(0, 0x0000A203)
#cpu.step()
#print(f"x4  (LBU)   = {cpu.regs[4]}")

# LHU 
#mem.write32(0, 0x0000A303)
#cpu.step()
#print(f"x5  (LHU)   = {cpu.regs[5]}")

# ===============================
# STORE
# ===============================

# SB 
#mem.write32(0, 0x0010A023)
#cpu.step()

# SH 
#mem.write32(0, 0x0020A023)
#cpu.step()

# SW 
#mem.write32(0, 0x0030A023)
#cpu.step()
