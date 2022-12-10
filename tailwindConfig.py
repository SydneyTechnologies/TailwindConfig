import os
import argparse
import subprocess
import re
from utils import *
import shutil

# so what we would like to accomplish is to initialize tailwind in a project
# install node modules to run tailwindcss
# run the command tailwind init to create the configuration file for tailwind
# pass in a input css file or the CLI will generate a default input.css file
# specify target files to watch
# the output css file that will be created

DESCRIPTION = "CLI application for boostraping Tailwindcss to any project"
EPILOG = "Automation tool made in python by Sydney Idundun"
PROG = "py-tailwind"
CONFIG_FILE = "tailwind.config.js"
INPUT_TAILWIND_CLASSES = (
    "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n"
)
REMOVABLE_LIST = [
    "tailwind.config.js",
    "package-lock.json",
    "package.json",
    "dist/",
    "node_modules/",
]
LOGGER_FILE = "tailwind.config.py"
parser = argparse.ArgumentParser(prog=PROG, description=DESCRIPTION, epilog=EPILOG)

# adding positional and optional arguments to the CLI
parser.add_argument(
    "init",
    nargs="?",
    help="argument will run the default configuration of tailwind in the current working directory or remove config files",
)
# take in an input the location of the input.css file that will be used for tailwind
parser.add_argument(
    "-i",
    "--input",
    help="input argument specifies the input css file to be used during tailwind config",
)
# take in the directory for the output.css file to be generated by tailwind css
parser.add_argument(
    "-o",
    "--output",
    default="./dist/output.css",
    help="output argument specifies the output css file that will be generated by tailwind",
)
# take in the file directory containing user color palette that will be extended/replaced by tailwind
parser.add_argument(
    "-e",
    "--extend",
    help="this allows a color palette to be specified through a text file",
    required=False,
)


args = parser.parse_args()


def initialize():
    if args.start is not None:
        if args.start == "init":
            # here we want to start the logging of files
            ToggleLogger(True)
            subprocess.check_call("npm install -D tailwindcss", shell=True)
            subprocess.check_call("npx tailwindcss init", shell=True)
            configureContentList()
            generateOutputCss(args.input, args.output)
        if args.init == "delete":
            for i in REMOVABLE_LIST:
                if os.path.exists(i):
                    if "/" in i:
                        shutil.rmtree(i)
                    else:
                        os.remove(i)
    else:
        print("Run tailwindConfig -h to understand the appropriate use of the CLI")


def generateContentList():
    fileList = []
    # this function will find all the HTML and JSX files
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if (
                file.endswith(".html")
                or file.endswith(".jsx")
                or file.endswith(".tsx")
                or file.endswith(".htm")
            ):
                path = os.path.relpath(root + f"/{file}")
                fileList.append(f"{path}")
    fileListString = ",\n".join(fileList)
    return fileListString, fileList


def configureContentList():
    # this function will configure the content list of
    # the tailwind.config.js file
    rConfigFile = open(CONFIG_FILE)
    configFile = rConfigFile.read()
    newConfig = None
    regex = r"content(.|\n|\r)*?],"
    result = re.finditer(regex, str(configFile), re.MULTILINE)
    for matchNum, match in enumerate(result, start=1):
        fileListString, fileList = generateContentList()
        globDirString, globDirList = globerizeList(fileList=fileList)
        globListString = f"content: [\n\t{minifyGlobDir(globDirList)}],"
        newConfig = configFile.replace(match.group(), globListString)
    with open(CONFIG_FILE, "w") as wConfigFile:
        wConfigFile.writelines(newConfig)


def generateOutputCss(input, output):
    # this function is responsible for generating the output css file
    # taking only the input, output locations
    # first we check if the input file exists
    if input is None:
        # generate the default input css file if no input file is specified
        default = "src/input.css"
        os.makedirs(os.path.dirname(default), exist_ok=True)
        with open(default, "w") as inputFile:
            inputFileObject = open(default, "r")
            inputFileContents = inputFileObject.read()
            if INPUT_TAILWIND_CLASSES not in inputFileContents:
                inputFile.write(INPUT_TAILWIND_CLASSES)
                print(f"Inserting Tailwind directives in {default} file")
            else:
                print("Tailwind directives already exist in this file")
            inputFileObject.close()
        input = default
    else:
        # if find(os.path.basename(input), os.getcwd()) is None:
        if os.path.exists(input) == False:
            print(f"The file {input} does not exist within current working directory")
        else:
            inputFileContents = open(input, "r").read()
            if INPUT_TAILWIND_CLASSES not in inputFileContents:
                prependLine(INPUT_TAILWIND_CLASSES, input)
            else:
                print(f"Tailwind directives already exist in {input} file")

    subprocess.check_call(f"npx tailwindcss -i {input} -o {output}", shell=True)
    ToggleLogger(False)


def updateContentList():
    configureContentList()


# fileListString, fileList = generateContentList()
# globDirString, globDirList = globerizeList(fileList=fileList)
# print(minifyGlobDir(globDirList))
initialize()

# print(find("input.css", os.getcwd()))
