"""
============================================================
Rekurzívna implementácia nedeterministického konečného automatu (NFA)

Každý stav automatu je reprezentovaný funkciou qX, ktorá:
- prijíma vstupný reťazec (string)
- vracia True, ak je reťazec akceptovaný z daného stavu
- vracia False inak

Nedeterministické vetvenie sa realizuje pomocou logického OR (or).

Epsilon-prechody sú reprezentované volaním inej funkcie
bez odoberania symbolu zo vstupného reťazca.
============================================================
"""


# ============================================================
# TODO:
# Implementuj počiatočný stav automatu.
#
# Príklad:
# def q0(string):
#     return q1(string) or q2(string)
# ============================================================
def q0(string: str) -> bool:
    # TODO: implementuj správanie počiatočného stavu
    pass


# ============================================================
# TODO:
# Implementuj jednotlivé stavy automatu (q1, q2, q3, ...)
#
# Odporúčanie:
# - najprv ošetri prípad prázdneho reťazca
# - potom spracuj prvý znak string[0]
# - pri prechode odober znak: string[1:]
# ============================================================


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
