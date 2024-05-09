from enum import Enum

def sign(val):
    if val < 0:
        return Sign.NEGATIVE
    elif val == 0: 
        return Sign.ZERO
    else:
        return Sign.POSITIVE

class Sign(Enum):
    NEGATIVE = -1,
    ZERO = 0,
    POSITIVE = 1
    