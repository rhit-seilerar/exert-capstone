from typing import cast
from pandare import Panda

class Context:
    def __init__(self, panda: Panda):
        self.panda = panda
        self.endianness = panda.endianness
        self.word_size = panda.bits // 8

    def read(self, address:int, size:int) -> (bytes | None):
        try:
            return cast(bytes, self.panda.virtual_memory_read(self.panda.get_cpu(), address, size))
        except ValueError:
            return None



    def parse_int(self, buf: (bytes | None), offset: int, size: int, signed: bool) -> (int | None):
        if buf is None:
            return None
        return int.from_bytes(buf[offset:offset+size], byteorder=self.endianness, signed=signed)

    def read_int(self, address: int, size: int, signed: bool) -> (int | None):
        return self.parse_int(self.read(address, size), 0, size, signed)

    def next_int(self, address: int, size: int, signed: bool) -> tuple[int | None, int]:
        val = self.read_int(address, size, signed)
        return val, address + size



    def parse_pointer(self, buf: (bytes | None), offset: int) -> (int | None):
        return self.parse_int(buf, offset, self.word_size, False)

    def read_pointer(self, address: int) -> (int | None):
        return self.parse_pointer(self.read(address, self.word_size), 0)

    def next_pointer(self, address: int) -> tuple[int | None, int]:
        return self.next_int(address, self.word_size, False)
