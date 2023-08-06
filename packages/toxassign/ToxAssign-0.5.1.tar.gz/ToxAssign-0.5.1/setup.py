# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toxassign']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.9,<4.0.0', 'pandas>=1.3.5,<2.0.0']

entry_points = \
{'console_scripts': ['toxassign = toxassign.Automation:main']}

setup_kwargs = {
    'name': 'toxassign',
    'version': '0.5.1',
    'description': 'A toxic assigner used to classify potentially toxic chemicals from a list of formulas of compounds.',
    'long_description': '# ToxAssign\n[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/swbreuer/ToxAssign/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/swbreuer/ToxAssign/?branch=main)\n[![Build Status](https://scrutinizer-ci.com/g/swbreuer/ToxAssign/badges/build.png?b=main)](https://scrutinizer-ci.com/g/swbreuer/ToxAssign/build-status/main)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![MOST logo](https://www.appropedia.org/w/images/thumb/c/c2/Sunhusky.png/240px-Sunhusky.png)](https://www.appropedia.org/Category:MOST)\n\n`ToxAssign` is designed to take the output of [MFAssignR](https://github.com/skschum/MFAssignR) and process the toxic compounds into an easily readable and understandable format.\n\nContents\n========\n\n * [Why?](#why)\n * [Installation](#installation)\n * [Usage](#usage)\n * [Output](#output)\n \n ### Why?\n \n&nbsp;&nbsp;&nbsp;This project has been designed in tandem with MOST\'s [BioPROTEIN project](https://www.appropedia.org/BioPROTEIN) to act as a precursor to live animal testing of completely novel food sources. This is intended to decrease the number of live animal tests required as to both decrease cost and increase ethical use of research resources. This project also seeks to serve as a useful tool in researching potential food sources for desperate times such as common agricultural wastes and potential future reprocessing research. To mee this goal this project uses entirely open source and free to use tools in its full workflow, including [MZMine](http://mzmine.github.io) and the previously mentioned [MFAssignR](https://github.com/skschum/MFAssignR).\n \n \n ### Installation\n The installation of this project is very simple.\n \n Install with [`pip3`](https://pypi.org/project/shallow-backup/)  \n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ pip3 install ToxAssign`\n\n### Usage\n&nbsp;&nbsp;&nbsp;To operate this tool, the user will need to place the csv files containing formulas they want to process in an empty folder along with the open food tox csv and the remove csv as in figure 29. The OpenFoodTox file contains the database of toxic compounds with their related formulas and the Remove file contains compounds that are not found on the PubChemClass database and thus are classified by hand.\n![Initial Folder Contents](./Images/InitialFolderContents.png?raw=true)\nThe formulas must match in format and must have a header above them labeled “formula” to be properly recognized. The files must also have the format of "(sign) (compound).csv" to be properly recognized. Then, the user will open a terminal window inside of the folder with the data to be processed and run the command toxassign. This will begin to output to the terminal with an output that looks similar to the following figure, starting with the name of the first compound to be processed followed by a print out of all the matched compounds and their assignment.\n![Output](./Images/output.png)\nFinally, there may be records that are not recognized by PubChemClass\'s database or are under a different name. To manage these a local database has been collated to deal with and categorize these compounds. When you classify unfound records, ensure to add them to the `Remove.csv` file for later use in the format already demonstrated in the file. The safety column falls into two broad categories: `safe`, determined by the keywords `safe`, `flavoring agent`, `fragrance`, or `supplement`; and as `other` determined by any other keywords.\n### Output\nOnce the code has terminated the directory will contain 4 new files and one directory per compound. The 4 new files, totalTox, totalToxFiltered, totalUnchecked, and totalUnfound, will contain all of the toxic records, all of the toxic records sorted by toxicity, all of the records not sorted, and all of the records not found in the PubChemClass database. \n![final folder contents](./Images/finalFolderContents.png)\nThe folders created by ToxAssign are each named after a compound delivered in the input. Each folder contains "+/- MainOut”, “+/- SetFound”, “+/- SetToxicFiltered”, “+/- SetUnchecked”, and “+/- SetUnfoundCopy”.\n![compound Folder Contents](./Images/compoundFolderContents.png)\nMainOut contains the compounds that either had a large unknown error, those that timed out when accessing the PubChemClass server, or those that were deemed safe by being food additives. \n![Main Out Contents](./Images/MainOutContents.png)\nSetFound contains compounds that were not found on PubChemClass but were identified in the list of compounds found by hand, sorted by unsafe and safe. \n![Set Found Contents](./Images/setFoundContents.png)\nSetUnchecked contains compounds that were found on PubChemClass but did not have enough information and SetUnfound contains compounds that were not found on PubChemClass or in the list of compounds found by hand. Finally SetToxic contains all the compounds that contain either safety classes or toxic records, at the top by acute toxicity and at the bottom containing their safety classes or no data for toxic records. \n![Set Toxic Contents](./Images/setToxicContents.png)\n',
    'author': 'Samuel Breuer',
    'author_email': 'swbreuer@mtu.edu',
    'maintainer': 'Samuel Breuer',
    'maintainer_email': 'swbreuer@mtu.edu',
    'url': 'https://github.com/swbreuer/ToxAssign',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
