# this python script contains utility functions used in the main CLI script [tailwindConfig.py]
import os 


# REGION generic functions
def find(name, path):
    # this function will find a specific file in a given directory
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def prependLine(line, initialFile):
    # this function is responsible for adding strings to the top of a file
    TEMPNAME = "tempfile.css"
    with open(TEMPNAME, "w") as writeObj, open(initialFile) as readObj:
        writeObj.write(line)
        for line in readObj:
            writeObj.write(line)
    os.remove(initialFile)
    os.rename(TEMPNAME, initialFile)

def globerizeList(fileList):
    # this function is will create a glob list of the provided file list
    glob_list = []
    globDir = ""
    for i in fileList:
        types = None
        dirName = os.path.dirname(i)
        if not glob_list.__contains__(dirName):
            if dirName == "":
                glob_list.append(f"\"{i}\"")
            else:
             glob_list.append("\"./" + dirName + "/**/*.{html, js, jsx, tsx, htm}\"")
    globDir = ",\n".join(glob_list)
    return globDir


def compareDir(stringA, stringB):
  lengthA = len(stringA)
  lengthB = len(stringB)
  result = ""
  obselete = None
  cap = 0  # this is where the for loop should stop
  # at the smallest string
  if lengthA < lengthB:
    cap = lengthA
  else:
    cap = lengthB

  for i in range(cap):
    if stringA[i] == stringB[i]:
      result += stringA[i]
    else:
      break

  if result.startswith("./") and result.endswith("/") and len(result) > 2:
    obselete = stringB if cap == lengthA else stringA

  return obselete


def minifyGlobDir(globedList):
    obseleteGlobList = []
    for i in range(len(globedList) - 1):
        for j in range(1, len(globedList) - 1):
            obseleteGlob = compareDir(globedList[i], globedList[j])
            if obseleteGlob != None:
                if not obseleteGlobList.__contains__(obseleteGlob):
                    obseleteGlobList.append(obseleteGlob)
    for i in obseleteGlobList:
        globedList.remove(i)

    print(globedList)
    return globedList




# ENDREGION

