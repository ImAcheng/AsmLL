class IResult:  # Represent an instruction result
    def __init__(self, sc: int, msg: str | None = None):
        self.status_code: int = sc
        self.message: str = msg