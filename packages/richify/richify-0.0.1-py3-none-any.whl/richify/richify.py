from sys import stdin, stderr, exit
from contextlib import suppress
from signal import signal, SIGINT, SIGTERM
from argparse import ArgumentParser
from rich.console import Console

def run():
    parser = ArgumentParser(description='Rich format arbitrary text input')
    parser.add_argument('--color', choices=['never', 'auto', 'always'], default='auto')
    args = parser.parse_args()
    console = Console(
        force_terminal=(args.color == 'always') or None,
        highlight=(args.color != 'never')
    )

    signal(SIGINT, lambda handler: exit(0))
    signal(SIGTERM, lambda handler: exit(0))

    for line in stdin:
        try:
            console.print(line, end='')
        except (BrokenPipeError, IOError):
            pass
            stderr.close()
            exit(0)

if __name__ == "__main__":
    run()