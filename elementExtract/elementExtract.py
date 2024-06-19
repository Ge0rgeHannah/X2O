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
            except Exception:
                pass
            if ns is not None:
                return ns
    return ns


# Identify all prefixes used within the schema
def findPrefixes(root):
    prefixes = []
    try:
        tagName = root.tagName
        prefix = tagName.split(":")[0]
        prefixes.append(prefix)
    except Exception:
        pass
    for child in root.childNodes:
        childPrefixes = findPrefixes(child)
        for p in childPrefixes:
            prefixes.append(p)
    return prefixes


def elementExtract(schemaPath):
    schema = dom.parse(schemaPath)

    root = schema.documentElement

    prefixes = findPrefixes(root)
    nsURIs = {prefix: resolveNameSpace(root, prefix) for prefix in prefixes}

    for prefix, ns in nsURIs.items():
        print(f"Namespace URI for prefix '{prefix}': {ns}")

    # ComplexTypes = schema.getElementsByTagName("xsd:complexType")
    # for i in ComplexTypes:
    #    print(i.getAttribute("name"))


if __name__ == "__main__":
    testSchemaPath = "../schemata/animl-core.xsd"
    elementExtract(testSchemaPath)
