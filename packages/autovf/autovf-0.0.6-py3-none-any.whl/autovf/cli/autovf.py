import argparse

from .. import __version__
from .predict import PredictAutoVFCommand
from .serve import ServeAutoVFCommand
from .train import TrainAutoVFCommand


def main():
    parser = argparse.ArgumentParser(
        "AutoVF CLI",
        usage="autovf <command> [<args>]",
        epilog="For more information about a command, run: `autovf <command> --help`",
    )
    parser.add_argument(
        "--version", "-v", help="Display AutoVF version", action="store_true"
    )

    commands_parser = parser.add_subparsers(help="commands")
    TrainAutoVFCommand.register_subcommand(commands_parser)
    PredictAutoVFCommand.register_subcommand(commands_parser)
    ServeAutoVFCommand.register_subcommand(commands_parser)

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    command = args.func(args)
    command.execute()


if __name__ == "__main__":
    main()
