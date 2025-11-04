from memory import Memory

mem = Memory(1024) 

mem.write32(0, 0x12345678)

val = mem.read32(0)

print(f"Valor lido: 0x{val:08X}")

print(f"Byte[0]: 0x{mem.read8(0):02X}")
print(f"Byte[1]: 0x{mem.read8(1):02X}")
print(f"Byte[2]: 0x{mem.read8(2):02X}")
print(f"Byte[3]: 0x{mem.read8(3):02X}")
