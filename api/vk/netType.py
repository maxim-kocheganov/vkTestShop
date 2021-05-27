
from enum import Enum

class NetType(Enum):
    dry = 0
    emulate = 1
    requests = 2
    requestsDebug = 3

class FakeServType(Enum):
    log = 0
    manual = 1
    auto = 2
