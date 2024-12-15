from exert.usermode.context import Context

class DummyPanda:
    def __init__(self, endianness = 'little', bits = 32, buf = b''):
        self.endianness = endianness
        self.bits = bits
        self.buf = buf

    def get_cpu(self):
        return None

    def virtual_memory_read(self, cpu, address, size):
        if address is None or address + size > len(self.buf):
            raise ValueError
        return self.buf[address:address+size]

def test_copy():
    context = Context(DummyPanda(), 0x4)
    context.suspend()
    context.address += 8

    copy_none = context.copy()
    assert context.panda == copy_none.panda
    assert context.endianness == copy_none.endianness
    assert context.word_size == copy_none.word_size
    assert context.address == copy_none.address
    assert len(copy_none.suspended) == 0

    copy_addr = context.copy(0x8)
    assert context.panda == copy_addr.panda
    assert context.endianness == copy_addr.endianness
    assert context.word_size == copy_addr.word_size
    assert copy_addr.address == 0x8
    assert len(copy_addr.suspended) == 0

def test_suspend():
    context = Context(DummyPanda(), 0x4)
    context.address += 3
    context.suspend()
    context.address += 4
    context.suspend()
    assert len(context.suspended) == 2
    assert context.suspended[0] == 4 + 3
    assert context.suspended[1] == 4 + 3 + 4

def test_apply():
    context = Context(DummyPanda(), 0x4)
    assert context.apply(0x77) == 0x77
    context.suspend()
    context.suspend()
    context.address += 8
    context.apply(True)
    assert len(context.suspended) == 1
    assert context.address == 12
    context.address += 3
    context.apply(False)
    assert len(context.suspended) == 0
    assert context.address == 4

def test_read():
    context = Context(DummyPanda(buf = b'\x05\x00\x00\x00'), 0x0)
    assert context.read(0x4, 4) is None
    assert context.read(0x0, 1) == b'\x05'

def test_int():
    context = Context(DummyPanda(buf = b'\x10\x00\x00\x00\xFE\xFF\xFF\xFF'), 0x4)
    assert context.parse_int(None, 4, 4, True) is None
    assert context.parse_int(context.panda.buf, 4, 4, True) == -2
    assert context.read_int(0x4, 1, False) == 254
    assert context.next_int(2, False) == 65534
    assert context.address == 6

def test_pointer():
    context = Context(DummyPanda(buf = b'\x10\x00\x00\x00\xFE\xFF\xFF\xFF'), 0x4)
    assert context.parse_pointer(context.panda.buf, 4) == 0xFFFFFFFE
    assert context.read_pointer(0x4) == 0xFFFFFFFE
    assert context.next_pointer() == 0xFFFFFFFE
    assert context.address == 8
