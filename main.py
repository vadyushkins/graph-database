import argparse

from src.algo.rpq import execute_rpq

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='command line interface for simple graph database')
    parser.add_argument(
        '--graph'
        , required=True
        , type=str
        , help='path to graph.txt file'
    )
    parser.add_argument(
        '--query'
        , required=True
        , type=str
        , help='path to query.txt file'
    )
    parser.add_argument(
        '--sources'
        , required=False
        , type=str
        , help='path to sources.txt file'
    )
    parser.add_argument(
        '--destinations'
        , required=False
        , type=str
        , help='path to destinations.txt file'
    )
    args = parser.parse_args()

    execute_rpq(args, verbose=True)
