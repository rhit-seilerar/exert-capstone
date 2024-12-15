class Context:
    def __init__(self, panda, address):
        self.panda = panda
        self.endianness = panda.endianness
        self.word_size = panda.bits // 8
        self.address = address
        self.suspended = []

    def copy(self, address = None):
        return Context(self.panda, self.address if address is None else address)

    def suspend(self):
        self.suspended.append(self.address)

    def apply(self, val):
        if len(self.suspended) > 0:
            old = self.suspended.pop()
            if not val:
                self.address = old
        return val

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

    def next_int(self, size, signed):
        val = self.read_int(self.address, size, signed)
        self.address += size
        return val



    def parse_pointer(self, buf, offset):
        return self.parse_int(buf, offset, self.word_size, False)

    def read_pointer(self, address):
        return self.parse_pointer(self.read(address, self.word_size), 0)

    def next_pointer(self):
        return self.next_int(self.word_size, False)
