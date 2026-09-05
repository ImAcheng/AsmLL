import os

import registers as _REG
from decoder import decoder
from custom_type import IResult

def interprete(fp: str) -> IResult:
    if not os.path.exists(fp):
        return IResult(-1, "File not found.")

    instructions: list[str]
    with open(fp) as file:
        instructions = file.readlines()

    # lable check
    _lables: list[str] = [inst for inst in instructions if inst.strip().endswith(":") and ' ' not in inst.strip()]
    for lb in _lables:
        if _lables.count(lb) > 1:
            return IResult(-1, f"Repeated lable found: {lb}")


    _REG.LBR = [(inst.strip().removesuffix(":"), instructions.index(inst)) for inst in _lables]

    LBR_IDXs: list[int] = [x[1] for x in _REG.LBR]

    while _REG.PC < len(instructions):
        if _REG.PC in LBR_IDXs:
            _REG.PC += 1
            continue

        line: str = instructions[_REG.PC]
        _REG.PC += 1

        if len(line.strip()) == 0 or line.strip().startswith(";"): 
            continue

        _dResult: IResult = decoder(line)

        if _dResult.status_code != 0:
            return IResult(_dResult.status_code, f"Error at line {_REG.PC}.\n{_dResult.message}")

    return IResult(0)
