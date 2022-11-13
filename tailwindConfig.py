import os
import argparse
import subprocess
import re
# so what we would like to accomplish is to initialize tailwind in a project
# install node modules to run tailwindcss
# run the command tailwind init to create the configuration file for tailwind
# pass in a input css file or the CLI will generate a default input.css file
# specify target files to watch
# the output css file that will be created 

# THINGS TO DO
# clean tailwind configuration, remove all the files regarding tailwind
# tailwind.config.js file, node modules, output file, input file containing tailwind base classes

# add the color palette feature with the color palette text file

# make the content list a findall file in folder list instead of the individual 

# update the content list again there should be a command for that

# create an update command that will update the content list, and the color palette if any
DESCRIPTION = "CLI application for boostraping Tailwindcss to any project"
EPILOG = "Automation tool made in python by Sydney Idundun"
PROG = "py-tailwind"
CONFIG_FILE = "tailwind.config.js"
INPUT_TAILWIND_CLASSES = "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n"

parser = argparse.ArgumentParser(prog=PROG, description=DESCRIPTION, epilog=EPILOG)

# adding positional and optional arguments to the CLI
# take in an input the location of the input.css file that will be used for tailwind
parser.add_argument("init", nargs='?', help="argument will run the default configuration of tailwind in the current working directory")
parser.add_argument("-i", "--input", help="input argument specifies the input css file to be used during tailwind config")
# take in the directory for the output.css file to be generated by tailwind css
parser.add_argument("-o", "--output", default="./dist/output.css", help="output argument specifies the output css file that will be generated by tailwind")
# take in the file directory containing user color palette that will be extended/replaced by tailwind
parser.add_argument("-e", "--extend", help="this allows a color palette to be specified through a text file", required=False)

def initialize():
    args = parser.parse_args()
    if args.init is not None:
        subprocess.check_call('npm install -D tailwindcss', shell=True)
        subprocess.check_call('npx tailwindcss init', shell=True)
        configureContentList()
        generateOutputCss(args.input, args.output)


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def generateContentList():
    result = []
    # this function will find all the HTML and JSX files
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".html") or file.endswith(".jsx") or file.endswith(".tsx") or file.endswith(".htm"):
                path = os.path.relpath(root + f"/{file}")
                result.append(f"{path}")
    content = ",\n".join(result)
    print(result)
    return content, result



def globerizeList(contentList):
    glob_list = []

    for i in contentList:
        types = None
        dirName = os.path.dirname(i)
        if not glob_list.__contains__(dirName):
            if dirName == "":
                glob_list.append(i)
            else:
             glob_list.append("\"./" + dirName + "/**/*.{html, js, jsx, tsx, htm}\"")
    return glob_list

def configureContentList():
    # this function will configure the content list of
    # the tailwind.config.js file
    rConfigFile = open(CONFIG_FILE)
    configFile =rConfigFile.read()
    newConfig = None
    regex = r"content(.|\n|\r)*?],"
    result = re.finditer(regex, str(configFile), re.MULTILINE)
    for matchNum, match in enumerate(result, start=1):
        content, contentList = generateContentList()
        contentListString = f"content: [\n{content}\n],"
        newConfig = configFile.replace(match.group(), contentListString)
    with open(CONFIG_FILE, "w") as wConfigFile:
        wConfigFile.writelines(newConfig)

def prependLine(line, initialFile):
    TEMPNAME = "tempfile.css"
    with open(TEMPNAME, "w") as writeObj, open(initialFile) as readObj:
        writeObj.write(line)
        for line in readObj:
            writeObj.write(line)
    os.remove(initialFile)
    os.rename(TEMPNAME, initialFile)


def generateOutputCss(input, output):
    # this function is responsible for generating the output css file
    # taking only the input, output locations 
    # first we check if the input file exists
    if input is None:
        # generate the default input css file if no input file is specified
        default="src/input.css"
        os.makedirs(os.path.dirname(default), exist_ok=True)
        with open(default, "w") as inputFile:
            inputFile.write(INPUT_TAILWIND_CLASSES)
        input = default
    else:
        if find(input, os.getcwd()) is None:
            print(f"The file {input} does not exist within current working directory")
        else:
            prependLine(INPUT_TAILWIND_CLASSES, input)
    
    subprocess.check_call(f"npx tailwindcss -i {input} -o {output} --watch", shell=True)

        

# initialize()

# test, list = generateContentList()
# for i in globerizeList(list):
#     print(i)
