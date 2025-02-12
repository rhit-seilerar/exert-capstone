from exert.usermode.context import Context

class DummyPanda:
    def __init__(self, buf = b'', endianness = 'little', bits = 32):
        self.buf = buf
        self.endianness = endianness
        self.bits = bits

    def get_cpu(self):
        return None

    def virtual_memory_read(self, cpu, address, size):
        if address is None or address + size > len(self.buf):
            raise ValueError
        return self.buf[address:address+size]

class DummyContext(Context):
    def __init__(self, buf = b'', endianness = 'little', bits = 32):
        super().__init__(DummyPanda(buf, endianness, bits))

def test_read():
    context = DummyContext(b'\x05\x00\x00\x00')
    assert context.read(0x4, 4) is None
    assert context.read(0x0, 1) == b'\x05'

def test_int():
    context = DummyContext(b'\x10\x00\x00\x00\xFE\xFF\xFF\xFF')
    assert context.parse_int(None, 4, 4, True) is None
    assert context.parse_int(context.panda.buf, 4, 4, True) == -2
    assert context.read_int(0x4, 1, False) == 254
    assert context.next_int(0x4, 2, False) == (65534, 0x6)

def test_pointer():
    context = DummyContext(b'\x10\x00\x00\x00\xFE\xFF\xFF\xFF')
    assert context.parse_pointer(context.panda.buf, 4) == 0xFFFFFFFE
    assert context.read_pointer(0x4) == 0xFFFFFFFE
    assert context.next_pointer(0x4) == (0xFFFFFFFE, 0x8)
