from typing import cast, Literal
from pandare import Panda
from exert.usermode.context import Context
from exert.utilities.types.multi_arch import CPUState

class DummyPanda(Panda):
    def __init__(self, buf: bytes = b'', # pylint: disable=W0231
                 endianness: Literal['little', 'big'] = 'little',  bits: int = 32):
        self.buf = buf
        self.endianness = endianness
        self.bits = bits

    def get_cpu(self) -> CPUState:
        return cast(CPUState, None)

    def virtual_memory_read(self, cpu: CPUState, addr: int, length: int,
                            fmt: str = 'bytearray') -> bytes:
        if addr is None or addr + length > len(self.buf):
            raise ValueError
        return self.buf[addr:addr+length]

class DummyContext(Context):
    def __init__(self, buf: bytes = b'', endianness: Literal['little', 'big'] = 'little',
                 bits: int = 32):
        self.panda: DummyPanda = DummyPanda(buf, endianness, bits)
        super().__init__(DummyPanda(buf, endianness, bits))

def test_read() -> None:
    context = DummyContext(b'\x05\x00\x00\x00')
    assert context.read(0x4, 4) is None
    assert context.read(0x0, 1) == b'\x05'

def test_int() -> None:
    context = DummyContext(b'\x10\x00\x00\x00\xFE\xFF\xFF\xFF')
    assert context.parse_int(None, 4, 4, True) is None
    assert context.parse_int(context.panda.buf, 4, 4, True) == -2
    assert context.read_int(0x4, 1, False) == 254
    assert context.next_int(0x4, 2, False) == (65534, 0x6)

def test_pointer() -> None:
    context = DummyContext(b'\x10\x00\x00\x00\xFE\xFF\xFF\xFF')
    assert context.parse_pointer(context.panda.buf, 4) == 0xFFFFFFFE
    assert context.read_pointer(0x4) == 0xFFFFFFFE
    assert context.next_pointer(0x4) == (0xFFFFFFFE, 0x8)
