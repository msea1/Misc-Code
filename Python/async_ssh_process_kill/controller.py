#!/usr/bin/python3
import argparse
import sys
from time import sleep


FILE_PATH = '/home/mcarruth/Temp/TEST_COUNT.txt'


class Runner:

    @staticmethod
    def run(attempt_num):
        print("Starting to run")
        i = 1 + 100 * attempt_num
        with open(FILE_PATH, "w") as count:
            for x in range(10):
                print(f"Writing {i}")
                count.writelines(f"{i}\n")
                count.flush()
                i += 1
                sleep(1)
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', required=True, help="iteration")
    args = parser.parse_args()

    try:
        print("in controller")
        runner = Runner()
        print("Runner made")
        result = runner.run(int(args.n))

        if not result:
            print("Runner returned False.")
            sys.exit(1)
    except Exception:
        print("Error occurred while trying to run a schedule")
        sys.exit(2)
