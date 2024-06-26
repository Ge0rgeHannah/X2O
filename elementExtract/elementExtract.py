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


def getComplexTypes(schema, xmlsPrefix):
    ComplexTypesBasic = schema.getElementsByTagName(
        xmlsPrefix + ":complexType")
    ComplexTypes = []
    seenComplexTypes = set()

    for e in ComplexTypesBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenComplexTypes:
                seenComplexTypes.add(name)
                ComplexTypes.append(e)

    print("-- complexType elements --")
    for i in ComplexTypes:
        print(i.getAttribute("name"))


def getSimpleTypes(schema, xmlsPrefix):
    SimpleTypesBasic = schema.getElementsByTagName(xmlsPrefix + ":simpleType")
    SimpleTypes = []
    seenSimpleTypes = set()

    for e in SimpleTypesBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenSimpleTypes:
                seenSimpleTypes.add(name)
                SimpleTypes.append(e)

    print("-- simpleType elements --")
    for i in SimpleTypes:
        print(i.getAttribute("name"))


def getAttributes(schema, xmlsPrefix):
    AttributesBasic = schema.getElementsByTagName(xmlsPrefix + ":attribute")
    Attributes = []
    seenAttributes = set()

    for e in AttributesBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenAttributes:
                seenAttributes.add(name)
                Attributes.append(e)

    print("-- attributes --")
    for i in Attributes:
        print(i.getAttribute("name"))


def getAttributeGroups(schema, xmlsPrefix):
    AttributeGroupsBasic = schema.getElementsByTagName(
        xmlsPrefix + ":attributeGroup")
    AttributeGroups = []
    seenAttributeGroups = set()

    for e in AttributeGroupsBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenAttributeGroups:
                seenAttributeGroups.add(name)
                AttributeGroups.append(e)

    print("-- attributeGroups --")
    for i in AttributeGroups:
        print(i.getAttribute("name"))


def elementExtract(schemaPath):
    schema = dom.parse(schemaPath)

    root = schema.documentElement

    prefixes = findPrefixes(root)
    nsURIs = {resolveNameSpace(root, prefix): prefix for prefix in prefixes}

    # for prefix, ns in nsURIs.items():
    #    print(f"Namespace is bound to: '{prefix}': {ns}")

    xmlsPrefix = nsURIs["http://www.w3.org/2001/XMLSchema"]

    # Identify complexType elements
    getComplexTypes(schema, xmlsPrefix)

    # Identify simpleType elements
    getSimpleTypes(schema, xmlsPrefix)

    # Identify attribute elements
    getAttributes(schema, xmlsPrefix)

    # Identify attributeGroup elements
    getAttributeGroups(schema, xmlsPrefix)


if __name__ == "__main__":
    testSchemaPath = "../schemata/animl-core.xsd"
    elementExtract(testSchemaPath)
