import os
from argparse import ArgumentError
from subprocess import CalledProcessError

import sys

from polidoro_argument import PolidoroArgumentParser
from polidoro_cli import CLI_DIR, VERSION
from polidoro_cli.cli.cli import load_clis


def main():
    # Load CLIs
    load_clis(CLI_DIR)

    parser = PolidoroArgumentParser(version=VERSION, prog='cli', raise_argument_error=True)
    try:
        parser.parse_args()
    except ArgumentError as err:
        sys.argv.insert(2, 'default_command')
        try:
            parser.parse_args()
        except ArgumentError:
            parser.error(str(err))
    except CalledProcessError as error:
        return error.returncode
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    os.environ['CLI_PATH'] = os.path.dirname(os.path.realpath(__file__))

    main()
