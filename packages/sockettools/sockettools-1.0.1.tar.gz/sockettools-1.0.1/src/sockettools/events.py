from types import FunctionType
from enum import Enum, EnumType

class _events(Enum):
    def __init__(self, handler):
        self.registered : dict[_events, list[FunctionType]] = dict()
        for _, event in type(self)._member_map_.items():
            self.registered[event] = []
    def _fire(self, event, *args, **kwargs):
        for func in self.registered[event]:
            func(*args, **kwargs)
    def register(self, event, func : FunctionType):
        self.registered[event].append(func)
    PACKET_RECIEVED = 0
    EXCEPTION = 1

_events : EnumType