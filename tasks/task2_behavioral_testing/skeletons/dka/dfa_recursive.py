"""
============================================================
Rekurzívna implementácia deterministického konečného automatu (DFA)

Každý stav automatu je reprezentovaný funkciou qX, ktorá:
- prijíma vstupný reťazec (string)
- vracia True, ak je reťazec akceptovaný z daného stavu
- vracia False inak
============================================================
"""


# ============================================================
# TODO:
# Implementuj počiatočný stav automatu.
#
# Príklad:
# def q0(string):
#         if len(string) > 0:
#         match string[0]:
#             case '0':
#                 return q1(string[1:])
#             case '1':
#                 return q2(string[1:])
#             case _:
#                 return False
#     return False
# ============================================================
def q0(string: str) -> bool:
    # TODO: implementuj správanie počiatočného stavu
    print('(q0, "{string}")') # Toto ma byt na začiatku každej funkcie
    pass


if __name__ == "__main__":
    """
    Testovacia časť – študent môže manuálne testovať automat.
    Táto časť NIE JE hodnotená.
    """

    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if q0(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
