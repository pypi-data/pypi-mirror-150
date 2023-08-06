import os
from argparse import ArgumentError
from subprocess import CalledProcessError

import sys
import yaml

from polidoro_argument import PolidoroArgumentParser
from polidoro_cli import CLI_DIR, CLI, VERSION


def read_yaml(file_name):
    with open(file_name) as file:
        return yaml.safe_load(file)


def load_clis(cli_dir):
    sys.path.insert(0, cli_dir)
    clis_py = []
    clis_cli = []
    clis_yaml = []
    for file in os.listdir(cli_dir):
        full_path = os.path.join(cli_dir, file)
        if os.path.isfile(full_path):
            if file.endswith('.yml') or file.endswith('.yaml'):
                clis_yaml.append(read_yaml(full_path))
            elif file.endswith('.py'):
                clis_py.append(file.replace('.py', ''))
            elif file.endswith('.cli'):
                clis_cli.append(full_path)

    # Load all <CLI>.py
    for py in clis_py:
        __import__(py)

    # Load all <CLI>.yml/yaml
    for cli in clis_yaml:
        CLI.create_yml_commands(cli)

    # Load all <CLI>.cli
    for cli in clis_cli:
        CLI.create_file_commands(cli)


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
