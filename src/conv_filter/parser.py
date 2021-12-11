import argparse


def run() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src', required=True)
    args = parser.parse_args()
    return args
