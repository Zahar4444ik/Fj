from core.regex.generators.fsa_generator import fsa_from_dka, fsa_from_nka
from tasks.task1_isomorphism.checker.compare import prepare_automaton_for_fsa_test, check_isomorphism, check_annotations


def evaluate_fsa(automaton, automaton_type):
    score = 0

    if automaton_type == "DKA":

        fsa_from_dka(automaton, filename="output/fsa/dka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/dka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_dka.fsa")
        if check_isomorphism(reference, student):
            print("DKA isomorphism test PASSED\n\t +8 points\n")
            score += 8
        else:
            print("DKA isomorphism test FAILED\n")
        if check_annotations(reference, student):
            print("DKA annotations test PASSED\n\t +2 points\n")
            score += 2
        else:
            print("DKA annotations test FAILED!")
            print("Expected:")
            print(reference.annotations_as_string())
            print("Received:")
            print(student.annotations_as_string())
    else:

        fsa_from_nka(automaton, filename="output/fsa/dka.fsa")

        reference = prepare_automaton_for_fsa_test("output/fsa/nka.fsa")
        student = prepare_automaton_for_fsa_test("tasks/student_io/fsa/student_nka.fsa")
        if check_isomorphism(reference, student):
            print("NKA isomorphism test PASSED\n\t +10 points\n")
            score += 10
        else:
            print("DKA isomorphism test FAILED\n")

    return score