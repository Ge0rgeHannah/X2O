import xml.dom.minidom as dom

# Import classes
from elementExtract.elementClasses import complexElement, simpleElement, tagAttribute, tagAttributeGroup


# Get text content from a node
def getNodeText(node):
    text = []
    for i in node.childNodes:
        if i.nodeType == i.TEXT_NODE:
            text.append(i.data)
    return "".join(text)


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

# TODO: Add code to capture more complex schema elements (e.g. restrictions)


# Populate complexType objects
def complexTypePopulation(element, schema, ns):
    conObj = complexElement()

    # Identify the root of the element
    allElements = schema.getElementsByTagName(ns + ":element")
    targetElement = None
    for i in allElements:
        if i.getAttribute("type") == element.getAttribute("name"):
            targetElement = i
    # if targetElement is None:
    #    raise Exception("No root element found for: " +
    #                    element.getAttribute("name"))

    # Get Name
    try:
        conObj.name = targetElement.getAttribute("name")
    except Exception:
        conObj.name = element.getAttribute("name")

    # Get Description

    # Check in type definition
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":annotation"):
            for j in i.childNodes:
                if j.nodeType == j.TEXT_NODE:
                    continue
                if j.getElementsByTagName(ns + ":documentation"):
                    conObj.description = getNodeText(j)

    # Check in root element
    if conObj.description == "":
        try:
            for i in targetElement.childNodes:
                if i.nodeType == i.TEXT_NODE:
                    continue
                if i.getElementsByTagName(ns + ":annotation"):
                    for j in i.childNodes:
                        if j.nodeType == i.TEXT_NODE:
                            continue
                        if j.getElementsByTagName(ns + ":documentation"):
                            conObj.description = getNodeText(j)
        except Exception:
            pass

    # Get attributeGroups
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":attributeGroup"):

            # Handle references
            if i.hasAttribute("ref"):
                conObj.attributeGroups.append(i.getAttribute("ref"))

            # Handle defined attributeGroups
            elif i.hasAttribute("name"):
                conObj.attributeGroups.append(i.getAttribute("name"))

    # Get attributes
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":attribute"):
            conObj.attributes.append(i.getAttribute("name"))

    # Get children
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":sequence"):
            for j in i.childNodes:
                if j.nodeType == j.TEXT_NODE:
                    continue
                if j.getElementsByTagName(ns + ":element"):

                    # Handle references
                    if j.hasAttribute("ref"):
                        conObj.children.append(j.getAttribute("ref"))

                    # Handle defined elements
                    if j.hasAttribute("name"):
                        conObj.children.append(j.getAttribute("name"))

    return conObj


# Populate simpleType objects
def simpleTypePopulation(element, schema, ns):
    conObj = simpleElement()

    # Identify the root of the element
    allElements = schema.getElementsByTagName(ns + ":element")
    targetElement = None
    for i in allElements:
        if i.getAttribute("type") == element:
            targetElement = i
    # if targetElement is None:
    #    raise Exception("No root element found for: " +
    #                    element.getAttribute("name"))

    # Get Name
    try:
        conObj.name = targetElement.getAttribute("name")
    except Exception:
        conObj.name = element.getAttribute("name")

    # Get Description

    # Check in type definition
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":annotation"):
            for j in i.childNodes:
                if j.nodeType == j.TEXT_NODE:
                    continue
                if j.getElementsByTagName(ns + ":documentation"):
                    conObj.description = getNodeText(j)

    # Check in root element
    try:
        if conObj.description == "":
            for i in targetElement.childNodes:
                if i.nodeType == i.TEXT_NODE:
                    continue
                if i.getElementsByTagName(ns + ":annotation"):
                    for j in i.childNodes:
                        if i.nodeType == i.TEXT_NODE:
                            continue
                        if j.getElementsByTagName(ns + ":documentation"):
                            conObj.description = getNodeText(j)
    except Exception:
        pass

    # Get Datatype
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":restriction"):
            if i.hasAttribute("base"):
                conObj.datatype = i.getAttribute("base")

    return conObj


# Populate attribute objects
def attributePopulation(element, schema, ns):
    conObj = tagAttribute()

    # Get Name
    conObj.name = element.getAttribute("name")

    # Get Description
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":annotation"):
            for j in i.childNodes:
                if j.nodeType == i.TEXT_NODE:
                    continue
                if j.getElementsByTagName(ns + ":documentation"):
                    conObj.description = getNodeText(j)

    # Get Datatype
    conObj.datatype = element.getAttribute("type")

    return conObj


# Populate attributeGroup objects
def attributeGroupPopulation(element, schema, ns):
    conObj = tagAttributeGroup()

    # Identify the root of the element
    allElements = schema.getElementsByTagName(ns + ":element")
    targetElement = None
    for i in allElements:
        if i.getAttribute("type") == element:
            targetElement = i
    # if targetElement is None:
    #    raise Exception("No root element found for: " +
    #                    element.getAttribute("name"))

    # Get Name
    try:
        conObj.name = targetElement.getAttribute("name")
    except Exception:
        conObj.name = element.getAttribute("name")
    conObj.name = element.getAttribute("name")

    # Get Description

    # Check in type definition
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":annotation"):
            for j in i.childNodes:
                if j.nodeType == j.TEXT_NODE:
                    continue
                if j.getElementsByTagName(ns + ":documentation"):
                    conObj.description = getNodeText(j)

    # Check in root element
    if conObj.description == "":
        try:
            for i in targetElement.childNodes:
                if i.nodeType == i.TEXT_NODE:
                    continue
                if i.getElementsByTagName(ns + ":annotation"):
                    for j in i.childNodes:
                        if j.nodeType == i.TEXT_NODE:
                            continue
                        if j.getElementsByTagName(ns + ":documentation"):
                            conObj.description = getNodeText(j)
        except Exception:
            pass

    # Get Attributes
    for i in element.childNodes:
        if i.nodeType == i.TEXT_NODE:
            continue
        if i.getElementsByTagName(ns + ":attribute"):
            conObj.attributes.append(i.getAttribute("name"))

    return conObj


def elementExtract(schemaPath):
    schemaPath = "schemata/" + schemaPath

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
        newComplexType = complexTypePopulation(i, schema, xmlsPrefix)
        elements.append(newComplexType)

    # simpleTypes
    for i in simpleTypes:
        newSimpleType = None
        newSimpleType = simpleTypePopulation(i, schema, xmlsPrefix)
        elements.append(newSimpleType)

    # attributes
    for i in attributes:
        newAttribute = None
        newAttribute = attributePopulation(i, schema, xmlsPrefix)
        elements.append(newAttribute)

    # attributeGroups
    for i in attributeGroups:
        newAttributeGroup = None
        newAttributeGroup = attributeGroupPopulation(i, schema, xmlsPrefix)
        elements.append(newAttributeGroup)


if __name__ == "__main__":
    testSchemaPath = "animl-core.xsd"
    elementExtract(testSchemaPath)
