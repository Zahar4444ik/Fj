import argparse

from core.assignment.quiz_generator import generate_quiz
import automated_testing.download_solutions as downloader
import automated_testing.evaluate_solutions as evaluator
import automated_testing.upload_results as uploader


def run_automated_pipeline():
    print("🚀 Starting full automated pipeline...")
    downloader.run()
    evaluator.run()
    uploader.run()
    print("✅ Full pipeline complete.")


def main():
    parser = argparse.ArgumentParser(description="FJ Assignment Management Tool")

    # Create subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("generate", help="Generate Moodle XML questions")
    subparsers.add_parser("download", help="Download solutions from Moodle")
    subparsers.add_parser("evaluate", help="Evaluate downloaded solutions")
    subparsers.add_parser("upload", help="Upload results back to Moodle")
    subparsers.add_parser("auto", help="Run full pipeline (Download -> Evaluate -> Upload)")

    args = parser.parse_args()

    # Map commands to functions
    if args.command == "generate":
        generate_quiz()
    elif args.command == "download":
        downloader.run()
    elif args.command == "evaluate":
        evaluator.run()
    elif args.command == "upload":
        uploader.run()
    elif args.command == "auto":
        run_automated_pipeline()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()