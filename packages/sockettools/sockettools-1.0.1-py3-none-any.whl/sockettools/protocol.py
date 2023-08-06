class _continue:
    def __eq__(self, __value) -> bool:
        return isinstance(__value, _continue)
    def __ne__(self, __value) -> bool:
        return not (self == __value)
CONTINUE = _continue()

class Protocol:
    @classmethod
    def encode(cls, data) -> bytearray:
        return data

    @classmethod
    def decode(cls, data : bytearray) -> object | _continue:
        return data