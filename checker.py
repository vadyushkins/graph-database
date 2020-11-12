import argparse

from pyformlang.cfg import *

from src.CYK import cyk
from src.RecursiveStateMachine import RecursiveStateMachine

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

    script = [Terminal(x) for x in script.replace(' ', '')]
    check = cyk(script, RecursiveStateMachine.from_txt('Syntax.txt').to_mycnf())

    print(f'SCRIPT IS {"VALID" if check else "NOT VALID"}')
