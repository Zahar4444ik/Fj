from automaton import DFA

if __name__ == "__main__":
    dfa = DFA()
    input_string = input ("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(f"Reťazec '{ input_string }' " 
              f"{'JE ' if dfa.check(input_string) else 'NIE JE '}akceptovaný!"
        )
        input_string = input ("Zadaj vstupný reťazec> ")