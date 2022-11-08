# TAILWIND CONFIG
We have made an automation tool too good to ignore. For developers who love using tailwind, tailwind config is for you.
### Introduction
Tailwind config is a CLI tool for bootstrapping tailwindcss to your next project. Configure tailwind with a simple command. No more adding glob patterns to the content list on tailwind.config.js file.
### Installing
Tailwind Config is currently unavailable on the python package index however the file will be uploaded as soon as the testing phase is completed.
However if you wish to test the currently build there is a build available on pythong test packing index
```
pip install -i https://test.pypi.org/simple/ tailwindConfig
```
### Quick Start
To quickly add tailwind to your project run the command below in the root directory of your project.
```
tailwindConfig init
```
This command will download all the node modules needed, create an input.css file within a folder called src. i.e  *src/input.css* and an output file within a folder called dist i.e *dist/output.css*. Edits the Tailwind.config.js file content list with all the Html, Js/Jsx files that exists in your current project.

However if you would like more control as to what your input file should be and where your output file should be generated. The tailwindconfig CLI takes in multiple arguments apart from init.
```
tailwindconfig [-h] [-i INPUT] [-o OUTPUT] [-e EXTEND] [init]
```
1. **-h** argument prints out a help to text to guide users learn tailwindConfig usage
2. **-i [input file location]** this argument takes in an input file location, specifying this file, will tell tailwindConfig to prepend the default tailwind classes in the file and use it to generate classes within the output css file.
>**NOTE:** *if this argument is not used tailwindConfig is going to generate an input css file in the path src/input.css*
3. **-o [ouput file location]**, this argument specifies the location of the tailwind output generated css file.
>**NOTE:** *if this argument is not used tailwindConfig is going to generate an input css file in the path src/input.css*
4. **-e [extended color file]**, this argument specifies the location of text color palette, tailwind config will add the color schemes specified in this color palette text file and will add it to tailwind.config.js file. 

**Don't Forget to Star this Repo!!!**

