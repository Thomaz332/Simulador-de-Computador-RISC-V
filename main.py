from memory import Memory
from cpu import CPU
from io_device import Io
from bus import Bus

mem = Memory(1024 * 1024)  # 1 MB de RAM
io = Io()
bus = Bus(mem, io)
cpu = CPU(bus)

mem = Memory(1024 * 1024)
io = Io()
bus = Bus(mem, io)
cpu = CPU(bus)

# setup de registradores iniciais
cpu.regs[1] = 10
cpu.regs[2] = 20

# instruções R-type (codificadas em hexadecimal)
mem.write32(0, 0x002081B3)  # ADD x3, x1, x2 → x3 = 30
mem.write32(4, 0x40208233)  # SUB x4, x1, x2 → x4 = -10
mem.write32(8, 0x0020F2B3)  # AND x5, x1, x2 → x5 = 0b1010 & 0b10100 = 0b0000
mem.write32(12, 0x0020E333) # OR  x6, x1, x2
mem.write32(16, 0x0020C3B3) # XOR x7, x1, x2

# executa 5 ciclos
for _ in range(5):
    cpu.step()

print(f"x3={cpu.regs[3]}, x4={cpu.regs[4]}, x5={cpu.regs[5]}, x6={cpu.regs[6]}, x7={cpu.regs[7]}")
