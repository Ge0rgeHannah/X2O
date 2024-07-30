# General imports
import argparse
import json

# Module imports
import elementExtract.elementExtract as elementExtract
import processComplexLabel.processComplexLabel as processComplexLabel


def run(args):

    schema = args.schema
    # Assign a default output that will cause an error if an invalid schema is provided
    output = None

    # Build pipeline from module list
    pipeline = []
    with open("pipeline.json", "r") as m:
        modulesJSON = json.load(m)
    modules = modulesJSON["modules"]
    for i in modules:
        item = {}
        try:
            item[i["moduleName"]] = i["arguments"]
        except Exception:
            item[i["moduleName"]] = ""
        pipeline.append(item)

    # Identify the correct stage in the pipeline and execute it
    for i in pipeline:
        for k, v in i.items():
            if k == "elementExtract":
                output = elementExtract.elementExtract(schema)
            elif k == "processComplexLabel":
                output = processComplexLabel.processComplexLabel(output)


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
