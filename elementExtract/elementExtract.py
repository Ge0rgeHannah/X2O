import xml.dom.minidom as dom

# Generate prefix to namespace bindings
def resolveNameSpace(element, prefix):
    ns = None
    if element.hasAttribute(f"xmlns:{prefix}"):
        ns = element.getAttribute(f"xmlns:{prefix}")
    else:
        if element.childNodes == []:
            return
        for child in element.childNodes:
            try:
                ns = resolveNameSpace(child, prefix)
            except:
                pass
            if ns is not None:
                return ns
    return ns

# TODO: Scan through the file to identify all prefixes used (so we can then look to generate bindings for them) (This will improve interoperability with other schemata
def findPrefixes():
    pass

def elementExtract(schemaPath):
    schema = dom.parse(schemaPath)

    root = schema.documentElement

    # TODO: Look into how namespaces are handled as abreviation can be different
    prefixesStr = input("Enter all prefixes used in the schema seperated by commas: ")
    prefixesStr = prefixesStr.replace(" ", "")
    print(prefixesStr)
    prefixes = prefixesStr.split(",")
    nsURIs = {prefix: resolveNameSpace(root, prefix) for prefix in prefixes}

    for prefix, ns in nsURIs.items():
        print(f"Namespace URI for prefix '{prefix}': {ns}")

    # ComplexTypes = schema.getElementsByTagName("xsd:complexType")
    # for i in ComplexTypes:
    #    print(i.getAttribute("name"))


if __name__ == "__main__":
    testSchemaPath = "../schemata/animl-core.xsd"
    elementExtract(testSchemaPath)
