import sys

import constants, interpreter

def print_help() -> None:
    sys.stdout.write("[AsmLL (Assembly-Like Programming Language)]\n" \
        "This language is inspired by 8051-Assembly.\n\n" \
        "[Commands]\n" \
        "help - display this list.\n"
        "version - display the version.\n" \
        "<file path> - run a AsmLL source file.")

def print_version() -> None:
    sys.stdout.write(f"[Version] {constants.__VERSION__}")

def main() -> None:
    _args: list[str] = sys.argv
    _arg0: str = _args[1]

    match _arg0:
        case "help":
            print_help()

        case "version":
            print_version()

        case _:
            iresult = interpreter.interprete(_arg0)
            if iresult.status_code != 0:
                sys.stdout.write(f"\nProgram ended with exit code {iresult.status_code}.\n{iresult.message}\n")

if __name__ == "__main__":
    main()