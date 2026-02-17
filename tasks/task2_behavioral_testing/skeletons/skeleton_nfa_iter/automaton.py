# TODO: Implementujte vami navrhnutý NFA ako triedu
# - konštruktor triedy nepreberá žiadne parametre len inicializuje atribúty triedy: transition_table, accepted_states, init_state a actual_state podľa špecifikácie NFA (to znamená, že každá inštancia tejto triedy bude predstavovať funkčnú implementáciu toho istého NFA)
# - trieda musí obsahovať verejnú metódu check, ktorá iteratívnym spôsobom zisťuje príslušnosť vstupného reťazca do jazyka
# - pre definíciu stavov možno použiť enumeračný typ Enum
# - DÔLEŽITÉ: v tomto skripte NIE JE POVOLENÉ využívať žiadnu rekurziu
# - manuálne testovanie riešenia je možné spustiť príkazom `py main.py` v adresári so súbormi riešenia

from enum import Enum, auto

class NFA:
    def __init__(self):
        pass

    def check(self, string: str) -> bool:
        pass