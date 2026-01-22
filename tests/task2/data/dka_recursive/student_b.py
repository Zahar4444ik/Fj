# "{0}"

def q0(string: str) -> bool:
    if len(string) == 0:
        return True
    else:
        match string[0]:
            case '0':
                return q0(string[1:])
            case _:
                return False
