class Rule:
    _cache = {}

    def ctest(self, context):
        return self.test(context, True)

    def test(self, context, clear_cache = False):
        if clear_cache:
            Rule._cache.clear()

        # For efficiency, we memoize the test() method by caching results
        pair = (self, context.address)
        if pair in Rule._cache:
            return Rule._cache[pair]

        # We may end up testing ourselves, so temporarily store True to pass the above check
        Rule._cache[pair] = True
        print(f'Testing {self}')
        result = self._test(context)
        Rule._cache[pair] = result
        return result

    def _test(self, context):
        return True

    def __str__(self):
        return 'Rule()'

class Int(Rule):
    def __init__(self, value, size = 4, signed = True):
        self.size = size
        self.signed = signed
        self.value = value

    def _test(self, context):
        context.suspend()
        val = context.next_int(self.size, self.signed)
        return context.apply(val == self.value)

    def __str__(self):
        return f'Int({self.value}, {self.size}, {self.signed})'

class Pointer(Rule):
    def __init__(self, rule):
        self.rule = rule

    def _test(self, context):
        context.suspend()

        # Test if the pointer points to a valid memory address
        pointer = context.next_pointer()
        data = context.read(pointer, 0)
        if pointer != 0 and data is None:
            print("Pointer is invalid: " + str(context.panda.buf))
            return context.apply(False)

        print("Pointer is valid")
        # Test futher rules against the found data
        new_ctx = context.copy(pointer)
        return context.apply(self.rule.test(new_ctx))

    def __str__(self):
        return f'Pointer({str(self.rule)})'

class Field(Rule):
    def __init__(self, name, rule):
        self.name = name
        self.rule = rule

    def _test(self, context):
        return self.rule.test(context)

    def __str__(self):
        return f'Field(\'{self.name}\', {str(self.rule)})'

class FieldGroup(Rule):
    def __init__(self, fields, optional=False):
        self.fields = fields
        self.optional = optional

    def _test(self, context):
        context.suspend()
        for field in self.fields:
            if not field.test(context):
                return context.apply(False)
        return context.apply(True)

    def __str__(self):
        return f'FieldGroup([{", ".join(str(f) for f in self.fields)}], {self.optional})'

class Struct(Rule):
    def __init__(self, name, field_groups):
        self.name = name
        self.field_groups = field_groups

    def _test(self, context):
        def helper(context, groups):
            if len(groups) == 0:
                return True
            context.suspend()
            group = groups[0]
            context_copy = context.copy()
            passes = group.test(context) and helper(context, groups[1:])
            if group.optional and helper(context_copy, groups[1:]):
                passes = True
                context = context_copy
            return context.apply(passes)
        return helper(context, self.field_groups)

    def __str__(self):
        return f'Struct(\'{self.name}\', [{", ".join(str(g) for g in self.field_groups)}])'

class _ListHead(Struct):
    def __init__(self):
        super().__init__('list_head', [FieldGroup([
            Field('next', Pointer(self)),
            Field('prev', Pointer(self))
        ])])

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

    def __str__(self):
        return 'ListHead()'
LIST_HEAD = _ListHead()

TASK_STRUCT = Rule()
