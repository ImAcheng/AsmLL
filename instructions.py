import sys
from time import sleep

from custom_type import *
import registers as reg
from iproc import *

# Dev log: Sep. 5, 2026
# planning to remove user_vars since I want this language to simulate asm

"""
    Special symbol meaning:
        # number
        $ string
        ; comment
"""

ALL_REGs = reg.program_registers.keys()

def aplp_mov(dest: str, src: str) -> IResult:
    return mov_hlper(dest, src) \
        if dest in ALL_REGs \
        else IResult(1, "Destination not found.")
    
def alpl_out(src: str) -> IResult:
    if src.startswith(("#", "$")):
        sys.stdout.write(src.removeprefix("#").removeprefix("$"))
        return IResult(0)

    if src in ALL_REGs:
        sys.stdout.write(str(reg.program_registers[src]))
    else:
        return IResult(1, "Destination not found.")
    
    return IResult(0)

def alpl_nl() -> IResult:
    sys.stdout.write("\n")
    return IResult(0)

def alpl_read(dest: str) -> IResult:
    if dest in ALL_REGs:
        reg.program_registers[dest] = input()
    else:
        return IResult(1, "Destination not found.")

    return IResult(0)

def alpl_add(dest: str, src: str) -> IResult:
    if src.startswith("#"):
        try:
            _num: int = int(src.removeprefix("#"))
            reg.program_registers[dest] += _num
        except ValueError:
            return IResult(1, "Value is not a number.")
        
    else:
        if dest in ALL_REGs:
            if src in ALL_REGs:
                try:
                    _num = reg.program_registers[src]
                    reg.program_registers[dest] += _num
                except TypeError:
                    return IResult(1, "Value is not a number.")

        else:
            return IResult(1, "Destination not found.")

    return IResult(0)

def alpl_sub(dest: str, src: str) -> IResult:
    if dest not in ALL_REGs:
        return IResult(1, "Destination not found.")

    if type(reg.program_registers[dest]) != int:
        return IResult(1, "Value is not a number.")

    if src.startswith("#"):
        try:
            _num: int = int(src.removeprefix("#"))
            reg.program_registers[dest] -= _num
        except ValueError:
            return IResult(1, "Value is not a number.")
        
    else:
        if src not in ALL_REGs:
            return IResult(1, "Source not found.")
        
        _num = reg.program_registers[src]
        if type(_num) != int:
            return IResult(1, "Value is not a number.")
            
        reg.program_registers[dest] -= _num

    return IResult(0)

def alpl_mul(a_reg: str, b_reg: str):
    if a_reg not in ALL_REGs or b_reg not in ALL_REGs:
        return IResult(1, "Invalid register.")

    if type(reg.program_registers[a_reg]) != int \
        or type(reg.program_registers[b_reg]) != int:
        return IResult(1, "Invalid value.")

    reg.program_registers[a_reg] *= reg.program_registers[b_reg]

    return IResult(0)

def alpl_div(a_reg: str, b_reg: str):
    if a_reg not in ALL_REGs or b_reg not in ALL_REGs:
        return IResult(1, "Invalid register.")

    if type(reg.program_registers[a_reg]) != int \
        or type(reg.program_registers[b_reg]) != int:
        return IResult(1, "Invalid value.")

    _i = reg.program_registers[a_reg] // reg.program_registers[b_reg]
    _r = reg.program_registers[a_reg] % reg.program_registers[b_reg]
    reg.program_registers[a_reg] = _i
    reg.program_registers[b_reg] = _r

    return IResult(0)

def alpl_jmp(dest: str) -> IResult:
    _target = next((x for x in reg.LBR if x[0] == dest), None)
    if _target is None:
        return IResult(1, f"Lable \"{dest}\" was not found.")

    reg.PC = _target[1]
    return IResult(0)

def alpl_delay(dt: str) -> IResult:
    """
    Normally, delay should be a loop in 8051 assembly,
    it works because we know the exact cpu cycle each instruction needs.
    But we're now in python, who knows lah.
    """

    ms: int = 0

    try:
        ms = int(dt)
    except ValueError:
        return IResult(1, "Value is not a number.")

    sleep(ms / 1000)

    return IResult(0)

def alpl_push(src: str) -> IResult:
    """
    You can only push a register.
    """

    if src not in ALL_REGs:
        return IResult(1, "No register found.")

    reg.STACK.append(reg.program_registers[src])

    return IResult(0)

def alpl_pop(dest: str) -> IResult:
    """
        You can only pop out to a register.
    """

    if dest not in ALL_REGs:
        return IResult(1, "Destination not found.")

    if len(reg.STACK) == 0:
        return IResult(1, "Stack is empty.")
    
    reg.program_registers[dest] = reg.STACK.pop()
    return IResult(0)

def alpl_call(dest: str) -> IResult:
    """
    Store the PC and jump to the destination.
    """

    reg.CALL_STACK.append(reg.PC)
    jmp_result = alpl_jmp(dest)

    if jmp_result.status_code != 0:
        reg.CALL_STACK.pop()

    return jmp_result

def alpl_ret() -> IResult:
    if len(reg.CALL_STACK) == 0:
        return IResult(1, "No place to return.")
    
    reg.PC = reg.CALL_STACK.pop()

    return IResult(0)

def alpl_bout(src: str) -> IResult:
    """
    must from register, print value as bits (number only)
    """

    if src not in ALL_REGs:
        return IResult(1, "Register not found.")

    _a = reg.program_registers[src]
    if not str(_a).isdigit():
        return IResult(1, "Value is not a number.")

    sys.stdout.write(f"{_a:032b}")

    return IResult(0)

def alpl_anl(dest: str, src: str) -> IResult:
    """
    must from register, and the value must be int
    """

    if dest not in ALL_REGs or \
        src not in ALL_REGs:
        return IResult(1, "Register not found.")

    _a = reg.program_registers[dest]
    _b = reg.program_registers[src]

    if not (type(_a) == int and type(_b) == int):
        return IResult(1, "Value is not a number.")

    reg.program_registers[dest] &= _b

    return IResult(0)

def alpl_orl(dest: str, src: str) -> IResult:
    """
    must from register, and the value must be int
    """

    if dest not in ALL_REGs or \
        src not in ALL_REGs:
        return IResult(1, "Register not found.")

    _a = reg.program_registers[dest]
    _b = reg.program_registers[src]

    if not (type(_a) == int and type(_b) == int):
        return IResult(1, "Value is not a number.")

    reg.program_registers[dest] |= _b

    return IResult(0)

def alpl_djnz(register: str, dest: str) -> IResult:
    """
        register value type must be a num
    """
    
    _sub = alpl_sub(register, "#1")
    if _sub.status_code != 0: return _sub

    if reg.program_registers[register] != 0:
        _jmp = alpl_jmp(dest)
        if _jmp.status_code != 0: return _jmp

    return IResult(0)

def alpl_cjne(register: str, data: str, dest: str) -> IResult:
    if register not in ALL_REGs:
        return IResult(1, "Register not found.")

    _reg_data = reg.program_registers[register]

    if data.startswith("#"):
        _tmp = int_conv(data.removeprefix("#"))

        if _tmp is None:
            return IResult(1, "Number is not convertable.")

        if _reg_data != _tmp:
            return alpl_jmp(dest)

        return IResult(0)

    if data.startswith("$"):
        _tmp = data.removeprefix("$")

        if _reg_data != _tmp:
            return alpl_jmp(dest)

        return IResult(0)

    # compare two same register's value, so they're same
    if register == data:
        return IResult(0)

    if data not in ALL_REGs:
        return IResult(1, "Register not found.")

    _data = reg.program_registers[data]

    if _reg_data != _data:
        return alpl_jmp(dest)

    return IResult(0)

def alpl_cpl(register: str) -> IResult:
    if register not in ALL_REGs:
        return IResult(1, "Register not found.")

    if type(reg.program_registers[register]) != int:
        return IResult(1, "Register doesn't store number.")

    reg.program_registers[register] ^= 0xFFFFFFFF

    return IResult(0)

def alpl_da(register: str) -> IResult:
    if register not in ALL_REGs:
            return IResult(1, "Register not found.")
    
    if type(reg.program_registers[register]) != int:
        return IResult(1, "Register doesn't store number.")

    reg.program_registers[register] = int(str(reg.program_registers[register]), 16)

    return IResult(0)