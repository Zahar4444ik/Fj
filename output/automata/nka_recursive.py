
"""
============================================================
Rekurzívna implementácia nedeterministického konečného automatu
Automat je generovaný automaticky zo syntaxového stromu regexu.
============================================================
"""


def q0(string: str) -> bool:
    return (len(string) > 0 and string[0] == 'eps' and q1(string[1:])) or (len(string) > 0 and string[0] == 'eps' and q3(string[1:]))


def q1(string: str) -> bool:
    return (len(string) > 0 and string[0] == '0' and q2(string[1:]))


def q10(string: str) -> bool:
    return len(string) == 0 or (len(string) > 0 and string[0] == 'eps' and q6(string[1:]))


def q2(string: str) -> bool:
    return len(string) == 0


def q3(string: str) -> bool:
    return (len(string) > 0 and string[0] == '1' and q4(string[1:]))


def q4(string: str) -> bool:
    return (len(string) > 0 and string[0] == 'eps' and q5(string[1:]))


def q5(string: str) -> bool:
    return len(string) == 0 or (len(string) > 0 and string[0] == 'eps' and q6(string[1:]))


def q6(string: str) -> bool:
    return (len(string) > 0 and string[0] == 'eps' and q7(string[1:])) or (len(string) > 0 and string[0] == 'eps' and q9(string[1:]))


def q7(string: str) -> bool:
    return (len(string) > 0 and string[0] == '1' and q8(string[1:]))


def q8(string: str) -> bool:
    return len(string) == 0 or (len(string) > 0 and string[0] == 'eps' and q6(string[1:]))


def q9(string: str) -> bool:
    return (len(string) > 0 and string[0] == '0' and q10(string[1:]))


if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if q0(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
