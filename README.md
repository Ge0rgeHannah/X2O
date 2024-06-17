# X2O: XSD to Ontology
A modular XSD to RDF translation pipeline

## Quickstart
To clone the clone the code, `cd` to the directory where you wish to save the code. Then run the command:

`git clone https://github.com/Ge0rgeHannah/X2O.git`

then run the command:

`cd X2O`

### Dependencies

To install the required dependencies, run the following command:

`pip install requirements.txt` or `pip3 install requirements.txt`

Make sure that `python 3.12.3` or newer is installed.

### Running the program

To run the program, run the following command:
`python main.py -s <schemafile.xsd>` or `python3 main.py -s <schemafile.xsd>`

`<schemafile.xsd>` is the filename of the XSD file that is being used as an input. The input file must be placed within the `schemata\` directory.

### Configuration

The X2O framework is modular and consists of x stages. Several stages have been included in this repository, however more can be added. This can be done through importing a PyPi package or by creating a package within this module in the following format:

```
X20
|   main.py
|   requirements.txt
|   pipeline.json
└---yourModule
|   |   __init__.py
|   |   yourModuleMethod.py
```

To allow your module to be used, add a line importing the module in `main.py`.

To define the modules used in the pipeline, select a set of modules from the list below (Make sure to pay attention to the input and output of each module), and add these modules in order to `pipeline.json`.

#### Modules

| Module Name | Description | Input | Output |
| ----------- | ----------- | ----- | ------ |
| XSD element ectractor | Identifies all elements and attributes in an XSD file and represents these concepts and their relations in an object stored in a list | XSD file | List of Element Objects |
| x | y | z | a |

## Project Structure

This project follows the following structure:

- `main.py` - This file is the "root" file, the program runs from this file and the modules are imported and combined into a pipeline here.
- `requirements.txt` - The dependencies for this project.
- `pipeline.json` - A list of the modules used for to construct the pipeline and their parameters.
- `schemata\` - A directory that XSD schemata are read from
- `output\` - A directory that the output of the pipeline is stored in
- `components\` - A directory holding other directories for components that modules rely on. E.g. `\models\` holds trained transformer models, `\APIs\` holds API keys for edifferent services
- `<module>\` - A directory for a pipeline module, following the structure described above.
