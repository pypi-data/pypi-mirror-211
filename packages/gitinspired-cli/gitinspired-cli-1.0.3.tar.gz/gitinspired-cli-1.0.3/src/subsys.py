import argparse
from src.file_manager import init, move_to_directory, mark_files, push_files, config

def main():
    parser = argparse.ArgumentParser(description="CLI tool for Gitinspired.")

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    config_parser = subparsers.add_parser("config", help="Configure settings")
    config_parser.add_argument("--code", help="Quiz code")
    config_parser.add_argument("--student_id", help="Student ID")

    init_parser = subparsers.add_parser("init", help="Initialize directory as an assignment submission")


    args = parser.parse_args()

    if args.subcommand == "config":
        config(args)
    elif args.subcommand == "init":
        init()
    else:
        print("Invalid command.")

if __name__ == "__main__":
    main()
