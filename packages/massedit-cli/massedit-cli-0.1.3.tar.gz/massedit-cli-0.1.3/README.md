# massedit-cli

Python mass editor CLI.

The missing entry point for [massedit](https://github.com/elmotec/massedit).

`massedit-cli` vendors `massedit` so that you can install it with `pipx` and use it<br/>
no matter which the python virtual env you're in the what `which python3` points to.

- [massedit-cli](#massedit-cli)
	- [Installation](#installation)
		- [pipx](#pipx)
		- [pip](#pip)
	- [Usage](#usage)
	- [Develop](#develop)

## Installation

### pipx

This is the recommended installation method.

```
$ pipx install massedit-cli
```


### [pip](https://pypi.org/project/massedit-cli/)

```
$ pip install massedit-cli
```

## Usage

Check out [massedit](https://github.com/elmotec/massedit) to learn more.

```
usage: massedit [-h] [-V] [-w] [-v] [-e EXPRESSIONS] [-f FUNCTIONS] [-x EXECUTABLES] [-s START_DIRS] [-m MAX_DEPTH] [-o FILE] [-g FILE] [--encoding ENCODING]
                [--newline NEWLINE]
                [file pattern ...]

Python mass editor

positional arguments:
  file pattern          shell-like file name patterns to process or - to read from stdin.

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -w, --write           modify target file(s) in place. Shows diff otherwise.
  -v, --verbose         increases log verbosity (can be specified multiple times)
  -e EXPRESSIONS, --expression EXPRESSIONS
                        Python expressions applied to target files. Use the line variable to reference the current line.
  -f FUNCTIONS, --function FUNCTIONS
                        Python function to apply to target file. Takes file content as input and yield lines. Specify function as [module]:?<function name>.
  -x EXECUTABLES, --executable EXECUTABLES
                        Python executable to apply to target file.
  -s START_DIRS, --start START_DIRS
                        Directory(ies) from which to look for targets.
  -m MAX_DEPTH, --max-depth-level MAX_DEPTH
                        Maximum depth when walking subdirectories.
  -o FILE, --output FILE
                        redirect output to a file
  -g FILE, --generate FILE
                        generate stub file suitable for -f option
  --encoding ENCODING   Encoding of input and output files
  --newline NEWLINE     Newline character for output files

Examples:
# Simple string substitution (-e). Will show a diff. No changes applied.
massedit -e "re.sub('failIf', 'assertFalse', line)" *.py

# File level modifications (-f). Overwrites the files in place (-w).
massedit -w -f fixer:fixit *.py

# Will change all test*.py in subdirectories of tests.
massedit -e "re.sub('failIf', 'assertFalse', line)" -s tests test*.py

# Will transform virtual methods (almost) to MOCK_METHOD suitable for gmock (see https://github.com/google/googletest).
massedit -e "re.sub(r'\s*virtual\s+([\w:<>,\s&*]+)\s+(\w+)(\([^\)]*\))\s*((\w+)*)(=\s*0)?;', 'MOCK_METHOD(\g<1>, \g<2>, \g<3>, (\g<4>, override));', line)" test.cpp

```


## Develop

```
$ git clone https://github.com/tddschn/massedit-cli.git
$ cd massedit-cli
$ poetry install
```