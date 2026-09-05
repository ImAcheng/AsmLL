"""
iproc.py (instruction processing helper)
This file contains functions that help instructions process sth
"""

from custom_type import IResult
import registers as _REG

def int_conv(val: str) -> int | None:
    _num: int | None = None
    try:
        match val[-1]:
            case 'B':
                _num = int(val.removesuffix("B"), 2)
            case 'H':
                _num = int(val.removesuffix("H"), 16)
            case _:
                _num = int(val, 10)
    except ValueError:
        return None

    return _num

def mov_hlper(dest: str, src: str) -> IResult:
    if dest not in _REG.program_registers.keys():
        return IResult(1, "Destination not found.")

    if src[0] == '#':
        _num = int_conv(src.removeprefix("#"))

        if _num is None:
            return IResult(1, "Value type doesn't match.")

        _REG.program_registers[dest] = _num    

    elif src[0] == '$':
        _word = src.removeprefix("$")
        _REG.program_registers[dest] =_word

    else:
        if src in _REG.program_registers.keys():
            _REG.program_registers[dest] = _REG.program_registers[src]
        else:
            return IResult(1, "Destination not found.")

    return IResult(0)