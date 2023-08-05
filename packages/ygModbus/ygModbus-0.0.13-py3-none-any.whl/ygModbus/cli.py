import argparse
from .server import run_server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['runserver'], help='Command to execute')
    args = parser.parse_args()

    if args.command == 'runserver':
        run_server()

if __name__ == '__main__':
    main()