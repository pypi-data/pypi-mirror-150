# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lice_tddschn', 'lice_tddschn.tests']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['lice = lice_tddschn.core:main']}

setup_kwargs = {
    'name': 'lice-tddschn',
    'version': '0.1.4',
    'description': 'Generate a license file for a project',
    'long_description': '# lice-tddschn\n\nFork of [Lice](https://github.com/licenses/lice), [original license](LICENSE-orig).\n\nlice-tddschn is made faster by not importing `pkg_resources` included in `setuptools`.\n\nLice generates license files. No more hunting down licenses from other\nprojects.\n\n- [lice-tddschn](#lice-tddschn)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Overview](#overview)\n  - [I want XXXXXXXXX license in here!](#i-want-xxxxxxxxx-license-in-here)\n  - [Usage](#usage)\n  - [Develop](#develop)\n\n## Installation\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install lice-tddschn\n```\n\n### [pip](https://pypi.org/project/lice-tddschn/)\n\n```\n$ pip install lice-tddschn\n```\n\n## Overview\n\nGenerate a BSD-3 license, the default:\n\n    $ lice\n    Copyright (c) 2013, Jeremy Carbaugh\n\n    All rights reserved.\n\n    Redistribution and use in source and binary forms, with or without modification,\n    ...\n\nGenerate an MIT license:\n\n    $ lice mit\n    The MIT License (MIT)\n    Copyright (c) 2013 Jeremy Carbaugh\n\n    Permission is hereby granted, free of charge, to any person obtaining a copy\n    ...\n\nGenerate a BSD-3 license, specifying the year and organization to be\nused:\n\n    $ lice -y 2012 -o "Sunlight Foundation"\n    Copyright (c) 2012, Sunlight Foundation\n\n    All rights reserved.\n\n    Redistribution and use in source and binary forms, with or without modification,\n    ...\n\nGenerate a BSD-3 license, formatted for python source file:\n\n    $ lice -l py\n\n    # Copyright (c) 2012, Sunlight Foundation\n    #\n    # All rights reserved.\n    #\n    # Redistribution and use in source and binary forms, with or without modification,\n    ...\n\nGenerate a python source file with a BSD-3 license commented in the\nheader:\n\n    $ lice -l py -f test\n    $ ls\n    test.py\n    $ cat test.py\n\n    # Copyright (c) 2012, Sunlight Foundation\n    #\n    # All rights reserved.\n    #\n    # Redistribution and use in source and binary forms, with or without modification,\n    ...\n\nGenerate a source file (language detected by -f extension):\n\n    $ lice -f test.c && cat test.c\n    /*\n     * Copyright (c) 2012, Sunlight Foundation\n     *\n     * All rights reserved.\n     *\n     * Redistribution and use in source and binary forms, with or without modification,\n    ...\n\nIf organization is not specified, lice will first attempt to use <span\nclass="title-ref">git config</span> to find your name. If not found, it\nwill use the value of the $USER environment variable. If the project\nname is not specified, the name of the current directory is used. Year\nwill default to the current year.\n\nYou can see what variables are available to you for any of the licenses:\n\n    $ lice --vars mit\n    The mit license template contains the following variables:\n      year\n      organization\n\n## I want XXXXXXXXX license in here!\n\nGreat! Is it a license that is commonly used? If so, open an issue or,\nif you are feeling generous, fork and submit a pull request.\n\n## Usage\n\n    usage: lice [-h] [-o ORGANIZATION] [-p PROJECT] [-t TEMPLATE_PATH] [-y YEAR]\n                [--vars] [license]\n\n    positional arguments:\n      license               the license to generate, one of: agpl3, apache, bsd2,\n                            bsd3, cddl, cc0, epl, gpl2, gpl3, lgpl, mit, mpl\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -o ORGANIZATION, --org ORGANIZATION\n                            organization, defaults to .gitconfig or\n                            os.environ["USER"]\n      -p PROJECT, --proj PROJECT\n                            name of project, defaults to name of current directory\n      -t TEMPLATE_PATH, --template TEMPLATE_PATH\n                            path to license template file\n      -y YEAR, --year YEAR  copyright year\n      -l LANGUAGE, --language LANGUAGE\n                            format output for language source file, one of: js, f,\n                            css, c, m, java, py, cc, h, html, lua, erl, rb, sh,\n                            f90, hpp, cpp, pl, txt [default is not formatted (txt)]\n      -f OFILE, --file OFILE Name of the output source file (with -l, extension can be omitted)\n      --vars                list template variables for specified license\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/lice-tddschn.git\n$ cd lice-tddschn\n$ poetry install\n```',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/lice-tddschn',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
