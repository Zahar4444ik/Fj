
"""
============================================================
Rekurzívna implementácia nedeterministického konečného automatu
Automat je generovaný automaticky zo syntaxového stromu regexu.
============================================================
"""


def q0(string: str) -> bool:
    return q1(string) or q9(string)


def q1(string: str) -> bool:
    return (len(string) > 0 and string[0] == 'e' and q2(string[1:]))


def q10(string: str) -> bool:
    return q3(string)


def q2(string: str) -> bool:
    return q3(string)


def q3(string: str) -> bool:
    return len(string) == 0 or q4(string)


def q4(string: str) -> bool:
    return q5(string) or q7(string)


def q5(string: str) -> bool:
    return (len(string) > 0 and string[0] == 'e' and q6(string[1:]))


def q6(string: str) -> bool:
    return len(string) == 0


def q7(string: str) -> bool:
    return (len(string) > 0 and string[0] == 'b' and q8(string[1:]))


def q8(string: str) -> bool:
    return len(string) == 0


def q9(string: str) -> bool:
    return (len(string) > 0 and string[0] == 'b' and q10(string[1:]))


if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if q0(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
