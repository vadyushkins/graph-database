import argparse

from pyformlang.cfg import *

from src.CYK import cyk
from src.RecursiveStateMachine import RecursiveStateMachine


def check(input_script):
    return cyk(
        [Terminal(x) for x in input_script.replace(' ', '')],
        RecursiveStateMachine.from_txt('Syntax.txt').to_mycnf()
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='script validator')
    parser.add_argument(
        '--script'
        , required=False
        , type=str
        , help='path to script.txt file'
        , default=None
    )
    args = parser.parse_args()

    script = ''
    if args.script is not None:
        script = ''
        with open(args.script, 'r') as f:
            for line in f:
                script += line.replace('\n', '')
    else:
        print('Please enter script:')
        while True:
            prev = len(script)
            script += input().replace('\n', '')
            if prev == len(script):
                break

    print(f'SCRIPT IS {"VALID" if check(script) else "NOT VALID"}')
