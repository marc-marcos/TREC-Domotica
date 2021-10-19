# <3

import json

def readData(file, attribName):
    f = open(file)
    data = json.load(f)

    f.close()
    return data[attribName]

def writeData(file, attribName, change):
    f = open(file)
    data = json.load(f)
    f.close()

    data[attribName] = change

    json_object = json.dumps(data)
    with open(file, 'w') as outfile:
        outfile.write(json_object)
        outfile.close()