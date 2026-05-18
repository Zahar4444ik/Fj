
"""
============================================================
Rekurzívna implementácia nedeterministického konečného automatu
Automat je generovaný automaticky zo syntaxového stromu regexu.
============================================================
"""


def q0(string: str) -> bool:
    return (len(string) > 0 and string[0] == '0' and q1(string[1:]))


def q1(string: str) -> bool:
    return len(string) == 0


if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if q0(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
