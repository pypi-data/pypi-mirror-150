# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['massedit_cli']

package_data = \
{'': ['*']}

install_requires = \
['massedit>=0.69.1,<0.70.0']

entry_points = \
{'console_scripts': ['massedit = massedit_cli:main']}

setup_kwargs = {
    'name': 'massedit-cli',
    'version': '0.1.2',
    'description': 'Python mass editor',
    'long_description': '# massedit-cli\n\nPython mass editor.\n\nThe missing entry point for [massedit](https://github.com/elmotec/massedit).\n\n`massedit-cli` vendors `massedit` so that you can install it with `pipx` and use it<br/>\nno matter which the python virtual env you\'re in the what `which python3` points to.\n\n- [massedit-cli](#massedit-cli)\n\t- [Installation](#installation)\n\t\t- [pipx](#pipx)\n\t\t- [pip](#pip)\n\t- [Usage](#usage)\n\t- [Develop](#develop)\n\n## Installation\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install massedit-cli\n```\n\n\n### [pip](https://pypi.org/project/massedit-cli/)\n\n```\n$ pip install massedit-cli\n```\n\n## Usage\n\nCheck out [massedit](https://github.com/elmotec/massedit) to learn more.\n\n```\nusage: massedit [-h] [-V] [-w] [-v] [-e EXPRESSIONS] [-f FUNCTIONS] [-x EXECUTABLES] [-s START_DIRS] [-m MAX_DEPTH] [-o FILE] [-g FILE] [--encoding ENCODING]\n                [--newline NEWLINE]\n                [file pattern ...]\n\nPython mass editor\n\npositional arguments:\n  file pattern          shell-like file name patterns to process or - to read from stdin.\n\noptions:\n  -h, --help            show this help message and exit\n  -V, --version         show program\'s version number and exit\n  -w, --write           modify target file(s) in place. Shows diff otherwise.\n  -v, --verbose         increases log verbosity (can be specified multiple times)\n  -e EXPRESSIONS, --expression EXPRESSIONS\n                        Python expressions applied to target files. Use the line variable to reference the current line.\n  -f FUNCTIONS, --function FUNCTIONS\n                        Python function to apply to target file. Takes file content as input and yield lines. Specify function as [module]:?<function name>.\n  -x EXECUTABLES, --executable EXECUTABLES\n                        Python executable to apply to target file.\n  -s START_DIRS, --start START_DIRS\n                        Directory(ies) from which to look for targets.\n  -m MAX_DEPTH, --max-depth-level MAX_DEPTH\n                        Maximum depth when walking subdirectories.\n  -o FILE, --output FILE\n                        redirect output to a file\n  -g FILE, --generate FILE\n                        generate stub file suitable for -f option\n  --encoding ENCODING   Encoding of input and output files\n  --newline NEWLINE     Newline character for output files\n\nExamples:\n# Simple string substitution (-e). Will show a diff. No changes applied.\nmassedit -e "re.sub(\'failIf\', \'assertFalse\', line)" *.py\n\n# File level modifications (-f). Overwrites the files in place (-w).\nmassedit -w -f fixer:fixit *.py\n\n# Will change all test*.py in subdirectories of tests.\nmassedit -e "re.sub(\'failIf\', \'assertFalse\', line)" -s tests test*.py\n\n# Will transform virtual methods (almost) to MOCK_METHOD suitable for gmock (see https://github.com/google/googletest).\nmassedit -e "re.sub(r\'\\s*virtual\\s+([\\w:<>,\\s&*]+)\\s+(\\w+)(\\([^\\)]*\\))\\s*((\\w+)*)(=\\s*0)?;\', \'MOCK_METHOD(\\g<1>, \\g<2>, \\g<3>, (\\g<4>, override));\', line)" test.cpp\n\n```\n\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/massedit-cli.git\n$ cd massedit-cli\n$ poetry install\n```',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/massedit-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
