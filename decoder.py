from custom_type import *
from instructions import *

# operation set: (op, argc)
_all_ops: dict[str, (IResult, int)] = {
    "mov": (aplp_mov, 2),
    "out": (alpl_out, 1),
    "nl": (alpl_nl, 0),
    "read": (alpl_read, 1),
    "add": (alpl_add, 2),
    "sub": (alpl_sub, 2),
    "mul": (alpl_mul, 2),
    "div": (alpl_div, 2),
    "jmp": (alpl_jmp, 1),
    "push": (alpl_push, 1),
    "pop": (alpl_pop, 1),
    "call": (alpl_call, 1),
    "ret": (alpl_ret, 0),
    "nop": (alpl_delay, 1),
    "bout": (alpl_bout, 1),
    "anl": (alpl_anl, 2),
    "orl": (alpl_orl, 2),
    "djnz": (alpl_djnz, 2),
    "cjne": (alpl_cjne, 3),
    "cpl": (alpl_cpl, 1),
    "da": (alpl_da, 1)
}

def decoder(line: str) -> IResult:
    # get the acutal instruction
    line = line.split(";", 1)[0].strip()

    parts = line.split(None, 1)
    opcode = parts[0].lower()

    opset = _all_ops.get(opcode)

    

    if opset is None:
        return IResult(-1, "Invalid instruction.")

    if len(parts) == 1:
        args = []
    else:
        args = [arg.strip() for arg in parts[1].split(",")]

    if len(args) != opset[1]:
        return IResult(-1, "Invalid instruction.")

    # print(f"[DECODER] {reg.PC} {args}")

    return opset[0](*args)