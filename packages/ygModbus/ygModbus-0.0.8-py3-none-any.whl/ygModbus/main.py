import argparse
from .server import run_server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ygModbus")
    subparsers = parser.add_subparsers(dest="command")

    runserver_parser = subparsers.add_parser("runserver", help="Run the server")

    args = parser.parse_args()

    if args.command == "runserver":
        run_server()