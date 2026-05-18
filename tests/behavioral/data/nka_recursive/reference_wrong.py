
"""
============================================================
Rekurzívna implementácia nedeterministického konečného automatu
Automat je generovaný automaticky zo syntaxového stromu regexu.
============================================================
"""


def q0(string: str) -> bool:
    return q1(string) or q4(string)


def q1(string: str) -> bool:
    return q2(string) or q8(string)


def q2(string: str) -> bool:
    return (len(string) > 0 and string[0] == '1' and q3(string[1:]))


def q3(string: str) -> bool:
    return q1(string) or q4(string)


def q4(string: str) -> bool:
    return (len(string) > 0 and string[0] == '0' and q5(string[1:]))


def q5(string: str) -> bool:
    return q6(string)


def q6(string: str) -> bool:
    return (len(string) > 0 and string[0] == '1' and q7(string[1:]))


def q7(string: str) -> bool:
    return len(string) == 0


def q8(string: str) -> bool:
    return (len(string) > 0 and string[0] == '0' and q9(string[1:]))


def q9(string: str) -> bool:
    return q1(string) or q4(string)


if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if q0(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
