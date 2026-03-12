from automaton import q0 # import funkcie q0 je potrebné nahradiť importom funkcie zodpovedajúcej začiatočnému stavu implementovaného NFA

if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        print(f"Reťazec '{input_string}' "
              f"{'JE ' if q0(input_string) else 'NIE JE '}akceptovaný!") # volanie funkcie q0 je potrebné nahradiť volaním funkcie zodpovedajúcej začiatočnému stavu implementovaného NFA
        input_string = input("Zadaj vstupný reťazec> ")