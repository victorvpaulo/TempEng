import sys
from pathlib import Path

current_path = Path(__file__).resolve()
test_src_path = current_path.parent
test_path = test_src_path.parent
project_path = test_path.parent
sys.path.append(str(test_src_path))
sys.path.append(str(test_path))
sys.path.append(str(project_path))

import argparse
import os
import integration_tests

parser = argparse.ArgumentParser(
    description="A utility to run the test suite for Template_Engine."
                "If executed without any arguments it will run the entire"
                " test suite.")

parser.add_argument("-u", "--unit", type=str, metavar="<test name>",
                    nargs="?", const="$all$",
                    help="Run unit tests. It can be used to run a"
                         " single unit test type by passing the test "
                         " type [compiler, executor or parser] as an argument"
                         " or all tests by passing no argument.")
parser.add_argument("-i", "--integration", type=str, metavar="<file path>",
                    nargs="?", const="$all$",
                    help="Run integration tests. It can be used to run a"
                         " single integration test case by passing the "
                         " path to the test case directory as an "
                         " argument, or all tests by passing no argument.")

args = parser.parse_args()

args_received = len(sys.argv)

all_integration_tests = False
all_unit_tests = False

if args_received < 2:
    all_integration_tests = True
    all_unit_tests = True
else:
    if args.integration == "$all$":
        all_integration_tests = True
    if args.unit == "$all$":
        all_unit_tests = True

if all_integration_tests:
    print("INTEGRATION TESTS: ")
    integration_tests.run_all_integration_tests()
elif args.integration is not None:
    print("INTEGRATION TEST: " + args.integration)
    integration_tests.run_integration_test(
        Path(args.integration).resolve())

if all_unit_tests:
    print("UNIT TESTS: ")
    os.system("python3 -m unittest")
elif args.unit is not None:
    print("UNIT TEST: " + args.unit)
    os.system("python3 -m unittest test_src.test_" + args.unit)
