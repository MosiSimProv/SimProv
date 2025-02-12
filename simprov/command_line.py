import argparse

from simprov.core import SimProv

parser = argparse.ArgumentParser(
    prog='simprov',
    description='Starts the SimProv provenance builder.')
parser.add_argument("pattern_specification", help="The path to the pattern specification file (YAML)")
parser.add_argument("rule_specification", help="The path to the rule specification file (PYTHON).")
parser.add_argument("--state-file", default="./study-state.pickle",
                    help="The path to the file storing the provenance information. Will be written using pickle.")


def main():
    print("SIMPROV")
    args = parser.parse_args()
    print(args)
    instance = SimProv(args.rule_specification, args.pattern_specification, args.state_file)
    # instance.load_study_state()
