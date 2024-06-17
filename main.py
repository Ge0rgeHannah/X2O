# General imports
import argparse
import json
import importlib

# Module imports
# import elementExtract
# import processComplexLabel


def run(args):

    # Build pipeline from module list
    pipeline: []
    with open("pipeline.json", "r") as m:
        modules = json.load(m)
    for i in modules:
        print(i)

    schema = args.schema


# Handle and bind arguments
def main():
    parser = argparse.ArgumentParser(
        prog="X2O",
        description="A modular XSD to ontology translation pipeline"
    )
    parser.add_argument(
        "-s",
        "--schema",
        type=str,
        help="The filename of the input XSD file",
        dest="schema",
        required=True
    )

    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
