class complexElement:
    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.attributeGroups = []
        self.attributes = []
        self.children = []


class simpleElement:
    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.datatype = ""


class tagAttribute:
    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.datatype = ""


class tagAttributeGroup:
    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.attributes = []
