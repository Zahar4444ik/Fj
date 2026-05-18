
"""
============================================================
Rekurzívna implementácia deterministického konečného automatu
Automat je generovaný automaticky zo syntaxového stromu regexu.
============================================================
"""


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


if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if q0(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
