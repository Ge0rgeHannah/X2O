import xml.dom.minidom as dom

# Import classes
from elementClasses import complexElement, simpleElement, tagAttribute, tagAttributeGroup


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
    complexTypesBasic = schema.getElementsByTagName(
        xmlsPrefix + ":complexType")
    complexTypes = []
    seenComplexTypes = set()

    for e in complexTypesBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenComplexTypes:
                seenComplexTypes.add(name)
                complexTypes.append(e)

    print("-- complexType elements --")
    for i in complexTypes:
        print(i.getAttribute("name"))

    return complexTypes


def getSimpleTypes(schema, xmlsPrefix):
    simpleTypesBasic = schema.getElementsByTagName(xmlsPrefix + ":simpleType")
    simpleTypes = []
    seenSimpleTypes = set()

    for e in simpleTypesBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenSimpleTypes:
                seenSimpleTypes.add(name)
                simpleTypes.append(e)

    print("-- simpleType elements --")
    for i in simpleTypes:
        print(i.getAttribute("name"))

    return simpleTypes


def getAttributes(schema, xmlsPrefix):
    attributesBasic = schema.getElementsByTagName(xmlsPrefix + ":attribute")
    attributes = []
    seenAttributes = set()

    for e in attributesBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenAttributes:
                seenAttributes.add(name)
                attributes.append(e)

    print("-- attributes --")
    for i in attributes:
        print(i.getAttribute("name"))

    return attributes


def getAttributeGroups(schema, xmlsPrefix):
    attributeGroupsBasic = schema.getElementsByTagName(
        xmlsPrefix + ":attributeGroup")
    attributeGroups = []
    seenAttributeGroups = set()

    for e in attributeGroupsBasic:
        if e.hasAttribute("name"):
            name = e.getAttribute("name")
            if name not in seenAttributeGroups:
                seenAttributeGroups.add(name)
                attributeGroups.append(e)

    print("-- attributeGroups --")
    for i in attributeGroups:
        print(i.getAttribute("name"))

    return attributeGroups


# Identify concepts that are not currently checked for
def collectUnknownElements(schema, conceptList, xmlsPrefix):
    level2Elements = schema.childNodes

    unknownElements = []

    elementTypeList = []
    for i in conceptList:
        if i.tagName not in elementTypeList:
            elementTypeList.append(i.tagName)

    for e in level2Elements:
        if e.nodeType == e.COMMENT_NODE:
            continue
        if e.tagName == (xmlsPrefix + ":element"):
            continue
        elif e.tagName in elementTypeList:
            continue
        else:
            unknownElements.append(e)

    # Print all unknown elements
    print("-- Unknown Elements --")
    for e in unknownElements:
        if e.hasAttribute("name"):
            print("Element: " + e.getAttribute("name") +
                  ", of type: " + e.tagName)

    return unknownElements

# TODO: Add code to populate the other fields

# Populate complexType objects
def complexTypePopulation(element, ns):
    conObj = complexElement()
    conObj.name = element
    return conObj


# Populate simpleType objects
def simpleTypePopulation(element, ns):
    conObj = simpleElement()
    conObj.name = element
    return conObj


# Populate attribute objects
def attributePopulation(element, ns):
    conObj = tagAttribute()
    conObj.name = element
    return conObj


# Populate attributeGroup objects
def attributeGroupPopulation(element, ns):
    conObj = tagAttributeGroup()
    conObj.name = element
    return conObj


def elementExtract(schemaPath):
    schema = dom.parse(schemaPath)

    root = schema.documentElement

    prefixes = findPrefixes(root)
    nsURIs = {resolveNameSpace(root, prefix): prefix for prefix in prefixes}

    # for prefix, ns in nsURIs.items():
    #    print(f"Namespace is bound to: '{prefix}': {ns}")

    xmlsPrefix = nsURIs["http://www.w3.org/2001/XMLSchema"]

    # Identify complexType elements
    complexTypes = getComplexTypes(schema, xmlsPrefix)

    # Identify simpleType elements
    simpleTypes = getSimpleTypes(schema, xmlsPrefix)

    # Identify attribute elements
    attributes = getAttributes(schema, xmlsPrefix)

    # Identify attributeGroup elements
    attributeGroups = getAttributeGroups(schema, xmlsPrefix)

    # Identify elements that don't fit into the above types
    knownConcepts = complexTypes + simpleTypes + attributes + attributeGroups
    edgeCases = collectUnknownElements(schema, knownConcepts, xmlsPrefix)

    # TODO: Implement some way of handeling the edge case elements 
    # (allowing the user to either ignore the elements, consider them as one 
    # of the other element types, or crash the program)

    # Generate the appropriate object for each concept
    elements = []

    # complexTypes
    for i in complexTypes:
        newComplexType = None
        newComplexType = complexTypePopulation(i, xmlsPrefix)
        elements.append(newComplexType)

    # simpleTypes
    for i in simpleTypes:
        newSimpleType = None
        newSimpleType = simpleTypePopulation(i, xmlsPrefix)
        elements.append(newSimpleType)

    # attributes
    for i in attributes:
        newAttribute = None
        newAttribute = attributePopulation(i, xmlsPrefix)
        elements.append(newAttribute)

    # attributeGroups
    for i in attributeGroups:
        newAttributeGroup = None
        newAttributeGroup = attributeGroupPopulation(i, xmlsPrefix)
        elements.append(newAttributeGroup)


if __name__ == "__main__":
    testSchemaPath = "schemata/MINiML.xsd"
    elementExtract(testSchemaPath)
