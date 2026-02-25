import download_solutions
import solution_evaluation
import uploading_results


def run():
    download_solutions.run()
    solution_evaluation.run()
    uploading_results.run()


if __name__ == "__main__":
    run()