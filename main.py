from memory import Memory
from io_device import Io
from bus import Bus
from cpu import CPU

mem = Memory()
io  = Io()
bus = Bus(mem, io)
cpu = CPU(bus)

cpu.regs[1] = 20
cpu.regs[2] = 10


print("\n=== MENU DE TESTES ===")
print("1 - ADD")
print("2 - SUB")
print("3 - AND")
print("4 - OR")
print("5 - XOR")
print("6 - SLT")
print("7 - SLTU")
print("8 - ADDI")
print("9 - ANDI")
print("10 - BEQ")
print("11 - BNE")
print("12 - LB")
print("13 - LW")
print("14 - SB")
print("15 - SH")
print("16 - SW")
print("17 - HELLO WORLD (IO)")

op = int(input("\nEscolha um teste: "))


# =======================================
#               R-TYPE
# =======================================
if op == 1:     # ADD
    mem.write32(0, 0x002081B3)
    cpu.step()
    print("x3 =", cpu.regs[3])

elif op == 2:   # SUB
    mem.write32(0, 0x40208233)
    cpu.step()
    print("x4 =", cpu.regs[4])

elif op == 3:   # AND
    mem.write32(0, 0x0020F2B3)
    cpu.step()
    print("x5 =", cpu.regs[5])

elif op == 4:   # OR
    mem.write32(0, 0x0020E333)
    cpu.step()
    print("x6 =", cpu.regs[6])

elif op == 5:   # XOR
    mem.write32(0, 0x0020C3B3)
    cpu.step()
    print("x7 =", cpu.regs[7])

elif op == 6:   # SLT
    mem.write32(0, 0x0020A533)
    cpu.step()
    print("x10 =", cpu.regs[10])

elif op == 7:   # SLTU
    mem.write32(0, 0x0020B5B3)
    cpu.step()
    print("x12 =", cpu.regs[12])

# =======================================
#             I-TYPE
# =======================================
elif op == 8:   # ADDI
    mem.write32(0, 0x00508593)
    cpu.step()
    print("x11 =", cpu.regs[11])

elif op == 9:   # ANDI
    mem.write32(0, 0x0050F613)
    cpu.step()
    print("x12 =", cpu.regs[12])

# =======================================
#             BRANCHES
# =======================================
elif op == 10:  # BEQ
    mem.write32(0, 0x00208663)
    cpu.step()
    print("PC =", cpu.pc)

elif op == 11:  # BNE
    mem.write32(0, 0x00209663)
    cpu.step()
    print("PC =", cpu.pc)

# =======================================
#               LOADS
# =======================================
elif op == 12:  # LB
    mem.write32(0, 0x0000A083)
    cpu.step()
    print("x1 =", cpu.regs[1])

elif op == 13:  # LW
    mem.write32(0, 0x0000A183)
    cpu.step()
    print("x3 =", cpu.regs[3])

# =======================================
#              STORES
# =======================================
elif op == 14:  # SB
    mem.write32(0, 0x0010A023)
    cpu.step()
    print("SB executado")

elif op == 15:  # SH
    mem.write32(0, 0x0020A023)
    cpu.step()
    print("SH executado")

elif op == 16:  # SW
    mem.write32(0, 0x0030A023)
    cpu.step()
    print("SW executado")

# =======================================
#            IO PROGRAMADO
# =======================================
elif op == 17:  # HELLO WORLD
    msg = "HELLO WORLD!\n"
    for i, c in enumerate(msg):
        bus.write8(0x80000 + i, ord(c))
    bus.write8(0x80000 + len(msg), 0)

    print("Executando 10 instruções para IO programado...")
    for _ in range(10):
        cpu.step()
