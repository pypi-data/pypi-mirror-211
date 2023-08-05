import argparse
from src.file_manager import move_to_directory, mark_files, push_files, config


def greet(args):
    if(args.name) == 'config':
        return config()

    message = f"Hello, {args.name}!"
    print(message)

    if args.directory:
        move_to_directory(args.directory)

    if args.mark:
        mark_files(args.mark)

    if args.push:
        push_files(args.push)

    if args.config:
        config()

def main():
    parser = argparse.ArgumentParser(description="CLI tool for greeting.")
    parser.add_argument("name", help="Name to greet")
    parser.add_argument("-d", "--directory", help="Move to directory")
    parser.add_argument("-m", "--mark", nargs="+", help="Mark files for capture")
    parser.add_argument("-p", "--push", help="Push marked files to server")
    parser.add_argument("-config", "--config", help="configure the repo.")
    args = parser.parse_args()
    greet(args)

if __name__ == "__main__":
    main()
