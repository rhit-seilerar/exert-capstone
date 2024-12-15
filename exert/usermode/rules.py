from collections import namedtuple

class Rule:
    _cache = {}

    def test(self, context):
        # For efficiency, we memoize the test() method by caching results
        pair = (self, context.address)
        if pair in Rule._cache:
            return Rule._cache[pair]

        # We may end up testing ourselves, so temporarily store True to pass the above check
        Rule._cache[pair] = True
        result = self._test(context)
        Rule._cache[pair] = result
        return result

    def _test(self, context):
        return True

class Int(Rule):
    def __init__(self, value, size = 4, signed = True):
        self.size = size
        self.signed = signed
        self.value = value

    def _test(self, context):
        context.suspend()
        val = context.next_int(self.size, self.signed)
        return context.apply(val == self.value)

class Pointer(Rule):
    def __init__(self, rule):
        self.rule = rule

    def _test(self, context):
        context.suspend()

        # Test if the pointer points to a valid memory address
        pointer = context.next_pointer()
        data = context.read(pointer, 0)
        if pointer != 0 and data is None:
            return context.apply(False)

        # Test futher rules against the found data
        new_ctx = context.copy(pointer)
        return context.apply(self.rule.test(new_ctx))

Field = namedtuple('Field', 'name rule')

class Struct(Rule):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def _test(self, context):
        context.suspend()
        for field in self.fields:
            if not field.rule.test(context):
                return context.apply(False)
        return context.apply(True)

class ListHead(Struct):
    def __init__(self):
        super().__init__('list_head', [
            Field('next', Pointer(self)),
            Field('prev', Pointer(self))
        ])

    def _test(self, context):
        context.suspend()
        if not super()._test(context):
            return context.apply(False)
        context.apply(False)

        # Validate that neighboring list heads maintain a full loop
        context.suspend()
        address = context.address

        next_pointer = context.next_pointer()
        next_prev_address = next_pointer + context.word_size
        next_prev_pointer = context.read_pointer(next_prev_address)

        prev_pointer = context.next_pointer()
        prev_next_address = prev_pointer + 0
        prev_next_pointer = context.read_pointer(prev_next_address)

        valid = next_prev_pointer == address and prev_next_pointer == address
        return context.apply(valid)
