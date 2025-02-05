from enum import Enum


class IndexType(str, Enum):
    """Imdex Type"""
    Kp = "Kp"
    Hp30 = "Hp30"
    Hp60 = "Hp60"
    ap = "ap"
    Ap = "Ap"
    Cp = "Cp"
    C9 = "C9"
    ap30 = "ap30"
    ap60 = "ap60"
    SN = "SN"
    Fobs = "Fobs"
    Fadj = "Fadj"


class StateType(str, Enum):
    """State Type"""
    DEFINED = "def"
    PREDICTED = "pre"
    ALL = "all"
