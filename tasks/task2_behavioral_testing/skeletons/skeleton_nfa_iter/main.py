from automaton import NFA

if __name__ == "__main__":
    nfa = NFA()
    input_string = input ("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print (f"Reťazec '{ input_string }' " 
               f"{'JE ' if nfa.check(input_string) else 'NIE JE '}akceptovaný!")
        input_string = input ("Zadaj vstupný reťazec> ")