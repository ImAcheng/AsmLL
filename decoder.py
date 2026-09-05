from custom_type import *
from instructions import *

def decoder(line: str) -> IResult:
    _cmt_inst = line.split(";")
    _op_arg = _cmt_inst[0].strip().split(" ", 1)
    _opcode = _op_arg[0].lower()
    _args: list[str] = [] if len(_op_arg) == 1 \
        else [arg.strip() for arg in _op_arg[1].split(",")]

    match _opcode:
        case "mov":
            return aplp_mov(_args[0], _args[1]) if len(_args) == 2 \
                else IResult(1, "Args don't match the instruction.") 

        case "out":
            return alpl_out(_args[0]) if len(_args) == 1 \
                else IResult(1, "Args don't match the instruction.")

        case "nl":
            return alpl_nl() if len(_args) == 0 else \
                IResult(1, "Args don't match the instruction.")

        case "read":
            return alpl_read(_args[0]) if len(_args) == 1 else \
                IResult(1, "Args don't match the instruction.")

        case "add":
            return alpl_add(_args[0], _args[1]) if len(_args) == 2 else \
                IResult(1, "Args don't match the instruction.")

        case "sub":
            return alpl_sub(_args[0], _args[1]) if len(_args) == 2 else \
                IResult(1, "Args don't match the instruction.")

        case "jmp":
            return alpl_jmp(_args[0]) if len(_args) == 1 else \
                IResult(1, "Args don't match the instruction.")

        case "push":
            return alpl_push(_args[0]) if len(_args) == 1 else \
                IResult(1, "Args don't match the instruction.")

        case "pop":
            return alpl_pop(_args[0]) if len(_args) == 1 else \
                IResult(1, "Args don't match the instruction.")

        case "call":
            return alpl_call(_args[0]) if len(_args) == 1 else \
                IResult(1, "Args don't match the instruction.")

        case "ret":
            return alpl_ret() if len(_args) == 0 else \
                IResult(1, "Args don't match the instruction.")

        case "nop":
            return alpl_delay(_args[0]) if len(_args) == 1 else \
                IResult(1, "Args don't match the instruction.")
        
        case "bout":
            return alpl_bout(_args[0]) if len(_args) == 1 else \
                IResult(1, "Args don't match the instruction.")
        
        case "anl":
            return alpl_anl(_args[0], _args[1]) if len(_args) == 2 else \
                IResult(1, "Args don't match the instruction.")

        case "orl":
            return alpl_orl(_args[0], _args[1]) if len(_args) == 2 else \
                IResult(1, "Args don't match the instruction.")

        case "djnz":
            return alpl_djnz(_args[0], _args[1]) if len(_args) == 2 else \
                IResult(1, "Args don't match the instruction.")

        case _:
            return IResult(1, "Unknown instruction.")