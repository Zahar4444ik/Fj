from enum import Enum, auto


# ============================================================
# TODO:
# Definuj všetky stavy nedeterministického konečného automatu.
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


class NFA:
    """
    Trieda reprezentujúca nedeterministický konečný automat (NFA)
    s iteratívnym spracovaním vstupného reťazca.
    """

    def __init__(self, transition_table: dict, accepted_states: set, init_state: State):
        """
        Konštruktor automatu.

        :param transition_table: tabuľka prechodov vo forme:
            (stav, symbol) -> množina stavov
            symbol '' reprezentuje epsilon prechod
        :param accepted_states: množina akceptačných stavov
        :param init_state: počiatočný stav automatu
        """
        self.transition_table = transition_table
        self.accepted_states = accepted_states
        self.init_state = init_state

        # Zásobník konfigurácií (stav, zvyšok vstupného reťazca)
        self.stack = None

    def expand_actual_configuration(self, actual_state: State, string: str) -> None:
        """
        TODO:
        Rozšír aktuálnu konfiguráciu automatu.

        Metóda má:
        - spracovať prechod podľa prvého znaku vstupného reťazca
        - spracovať epsilon-prechody (bez čítania znaku)
        - nové konfigurácie uložiť do zásobníka self.stack

        :param actual_state: aktuálny stav automatu
        :param string: zvyšok vstupného reťazca
        """
        # TODO: implementuj rozšírenie konfigurácie
        pass

    def check(self, string: str) -> bool:
        """
        TODO:
        Over, či automat akceptuje zadaný vstupný reťazec.

        Algoritmus má byť iteratívny a má používať zásobník:
        1. Inicializuj zásobník počiatočnou konfiguráciou
        2. Kým zásobník nie je prázdny:
           - vyber konfiguráciu
           - ak je stav akceptačný a reťazec je prázdny → ACCEPT
           - inak rozšír konfiguráciu
        3. Ak sa žiadna akceptačná konfigurácia nenájde → REJECT

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
    - definuj množinu akceptačných stavov
    - vytvor inštanciu NFA
    - otestuj automat na rôznych vstupných reťazcoch
    ============================================================
    """

    # TODO: definuj transition_table
    transition_table = {}

    # TODO: definuj množinu akceptačných stavov
    accepted_states = set()

    # TODO: vytvor automat
    nfa = NFA(transition_table=transition_table,
              accepted_states=accepted_states,
              init_state=State.q0)

    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(f"Reťazec '{input_string}' "
              f"{'JE ' if nfa.check(input_string) else 'NIE JE '}akceptovaný!")
        input_string = input("Zadaj vstupný reťazec> ")
