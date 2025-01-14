class Context:
    def __init__(self, panda):
        self.panda = panda
        self.endianness = panda.endianness
        self.word_size = panda.bits // 8

    def read(self, address, size):
        try:
            return self.panda.virtual_memory_read(self.panda.get_cpu(), address, size)
        except ValueError:
            return None



    def parse_int(self, buf, offset, size, signed):
        if buf is None:
            return None
        return int.from_bytes(buf[offset:offset+size], byteorder=self.endianness, signed=signed)

    def read_int(self, address, size, signed):
        return self.parse_int(self.read(address, size), 0, size, signed)

    def next_int(self, address, size, signed):
        val = self.read_int(address, size, signed)
        return val, address + size



    def parse_pointer(self, buf, offset):
        return self.parse_int(buf, offset, self.word_size, False)

    def read_pointer(self, address):
        return self.parse_pointer(self.read(address, self.word_size), 0)

    def next_pointer(self, address):
        return self.next_int(address, self.word_size, False)
