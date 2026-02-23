# "{0}"

def q0(string: str) -> bool:
    return len(string) == 0 or (len(string) > 0 and string[0] == 'eps' and q1(string[1:]))


def q1(string: str) -> bool:
    return (len(string) > 0 and string[0] == '0' and q2(string[1:]))


def q2(string: str) -> bool:
    return len(string) == 0 or (len(string) > 0 and string[0] == 'eps' and q1(string[1:]))
