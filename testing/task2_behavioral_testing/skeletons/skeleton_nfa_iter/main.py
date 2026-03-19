from automaton import NFA

if __name__ == "__main__":
    nfa = NFA()
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        result = nfa.check(input_string)
        if not isinstance(result, bool):
            print(f"TypeError: vrátilo {type(result).__name__} namiesto bool (hodnota: {result!r})")
        else:
            print(f"Reťazec '{input_string}' "
                  f"{'JE ' if result else 'NIE JE '}akceptovaný!")
        input_string = input("Zadaj vstupný reťazec> ")