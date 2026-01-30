def get_assignment_description(assignment):
    regex = assignment["regex"]
    automaton_type = assignment["automaton_type"]
    implementation = assignment["implementation"]
    return f"""
        Vašou úlohou je navrhnúť konečnostavový automat a naprogramovať jeho implementáciu
        pre akceptáciu slov jazyka špecifikovaného nasledujúcim regulárnym výrazom:
        
            R = {regex}
        
        Typ automatu: {automaton_type}
        Spôsob implementácie: {implementation}
        
        Navrhnite {automaton_type} konečnostavový automat,
        ktorý rozpoznáva jazyk definovaný regulárnym výrazom R, a zapíšte ho
        do súboru vo formáte .fsa.
        
        Následne doplňte kostru programu tak, aby metóda:
        
            check(word: str) -> bool
        
        správne určovala, či dané slovo patrí do daného jazyka.
        
        Nie je povolené používať externé knižnice ani meniť štruktúru riešenia.

    """
