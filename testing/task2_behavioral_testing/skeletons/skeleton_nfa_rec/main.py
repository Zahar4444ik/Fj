from automaton import q0 # import funkcie q0 je potrebné nahradiť importom funkcie zodpovedajúcej začiatočnému stavu implementovaného NFA

if __name__ == "__main__":
    input_string = input("Zadaj vstupný reťazec> ")
    while input_string != "quit":
        result = q0(input_string)  # volanie funkcie q0 je potrebné nahradiť volaním funkcie zodpovedajúcej začiatočnému stavu implementovaného NFA
        if not isinstance(result, bool):
            print(f"TypeError: vrátilo {type(result).__name__} namiesto bool (hodnota: {result!r})")
        else:
            print(f"Reťazec '{input_string}' "
                  f"{'JE ' if result else 'NIE JE '}akceptovaný!")
        input_string = input("Zadaj vstupný reťazec> ")