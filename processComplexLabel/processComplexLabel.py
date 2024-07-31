import re


def processComplexLabel(cList):
    for i in cList:
        labelArray = []
        label = i.name
        labelArray.append(label)

        # Regex found at https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
        tokenLabel = re.sub('([A-Z][a-z]+)', r' \1',
                            re.sub('([A-Z]+)', r' \1', label)).split()

        print(tokenLabel)
        labelArray.append(tokenLabel)
        i.name = labelArray

    return (cList)


if __name__ == "__main__":
    conceptList = [
    ]
    processComplexLabel(conceptList)
