PC: int = 0 # program counter
LBR: list[tuple] = []  # lable register
STACK: list = [] # uh, this is a, stack, yeah
CALL_STACK: list[int] = [] # store where to return from call

# simulate what we have in 8051 ASM (R0 ~ R7 only).
program_registers: dict[str, int] = {
    "R0": None, "R1": None, "R2": None, "R3": None, "R4": None, "R5": None, "R6": None, "R7": None
}