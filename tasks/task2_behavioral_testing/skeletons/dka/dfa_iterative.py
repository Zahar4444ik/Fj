from enum import Enum, auto


# ============================================================
# TODO:
# Definuj všetky stavy deterministického konečného automatu (DFA).
# Každý stav má byť prvok enumu State.
#
# Príklad:
# class State(Enum):
#     q0 = auto()
#     q1 = auto()
#     ...
# ============================================================
class State(Enum):
    # TODO: doplň jednotlivé stavy automatu
    pass


class DFA:
    """
    Trieda reprezentujúca deterministický konečný automat (DFA)
    s iteratívnym spracovaním vstupného reťazca.
    """

    def __init__(self, transition_table: dict, accepted_states: set, init_state: State):
        """
        Konštruktor automatu.

        :param transition_table: tabuľka prechodov vo forme:
            (stav, symbol) -> stav
        :param accepted_states: množina akceptačných stavov
        :param init_state: počiatočný stav automatu
        """
        self.transition_table = transition_table
        self.accepted_states = accepted_states
        self.init_state = init_state

        # Aktuálny stav počas spracovania vstupu
        self.actual_state = None

    def check(self, string: str) -> bool:
        """
        TODO:
        Over, či automat akceptuje zadaný vstupný reťazec.

        Algoritmus má byť iteratívny:
        1. Nastav aktuálny stav na počiatočný stav
        2. Pre každý symbol vstupného reťazca:
           - ak existuje prechod (stav, symbol), vykonaj ho
           - inak → reťazec nie je akceptovaný
        3. Po spracovaní celého reťazca:
           - ak je aktuálny stav akceptačný → ACCEPT
           - inak → REJECT

        :param string: vstupný reťazec
        :return: True ak je reťazec akceptovaný, inak False
        """
        # TODO: implementuj kontrolu akceptácie reťazca
        pass


if __name__ == "__main__":
    """
    ============================================================
    TODO:
    V tejto časti:
    - definuj tabuľku prechodov
      Príklad formátu:
        transition_table = {
            (State.q0, '0'): State.q1,
            (State.q0, '1'): State.q2,
            ...
        }
    - definuj množinu akceptačných stavov
    - vytvor inštanciu DFA
    - otestuj automat na rôznych vstupných reťazcoch
    ============================================================
    """

    # TODO: definuj transition_table
    transition_table = {}

    # TODO: definuj množinu akceptačných stavov
    accepted_states = set()

    # TODO: definuj počiatočný stav
    init_state = None

    # TODO: vytvor automat
    dfa = DFA(
        transition_table=transition_table,
        accepted_states=accepted_states,
        init_state=init_state
    )

    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(
            f"Reťazec '{input_string}' "
            f"{'JE ' if dfa.check(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input("Zadaj vstupný reťazec> ")
