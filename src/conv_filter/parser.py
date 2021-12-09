import argparse


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src')
    args = parser.parse_args()

    print(f"{args.src=}")
