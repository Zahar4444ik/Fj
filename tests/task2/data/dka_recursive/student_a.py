# '0'

def q0(string: str) -> bool:
    if len(string) == 0:
        return False
    else:
        match string[0]:
            case '0':
                return q1(string[1:])
            case _:
                return False


def q1(string: str) -> bool:
    if len(string) == 0:
        return True
    else:
        match string[0]:
            case _:
                return False
