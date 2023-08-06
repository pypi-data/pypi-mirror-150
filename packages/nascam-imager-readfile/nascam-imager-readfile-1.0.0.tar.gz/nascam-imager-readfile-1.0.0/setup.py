# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nascam_imager_readfile']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14.0,<2.0.0', 'opencv-python>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'nascam-imager-readfile',
    'version': '1.0.0',
    'description': 'Read functions for NASCAM ASI raw files',
    'long_description': '# NASCAM All-Sky Imager Raw PGM Data Readfile\n\n[![Github Actions - Tests](https://github.com/ucalgary-aurora/nascam-imager-readfile/workflows/tests/badge.svg)](https://github.com/ucalgary-aurora/nascam-imager-readfile/actions?query=workflow%3Atests)\n[![PyPI version](https://img.shields.io/pypi/v/nascam-imager-readfile.svg)](https://pypi.python.org/pypi/nascam-imager-readfile/)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/ucalgary-aurora/nascam-imager-readfile/blob/main/LICENSE)\n[![PyPI Python versions](https://img.shields.io/pypi/pyversions/nascam-imager-readfile.svg)](https://pypi.python.org/pypi/nascam-imager-readfile/)\n\nPython library for reading NASCAM All-Sky Imager (ASI) stream0 raw PNG-file data. The data can be found at https://data.phys.ucalgary.ca.\n\n## Supported Datasets\n\n- NASCAM ASI raw: [stream0.png](https://data.phys.ucalgary.ca/sort_by_project/NORSTAR/nascam-msi/stream0.png) PNG files\n\n## Installation\n\nThe nascam-imager-readfile library is available on PyPI:\n\n```console\n$ python3 -m pip install nascam-imager-readfile\n```\n\n## Supported Python Versions\n\nnascam-imager-readfile officially supports Python 3.6+.\n\n## Examples\n\nExample Python notebooks can be found in the "examples" directory. Further, some examples can be found in the "Usage" section below.\n\n## Usage\n\nImport the library using `import nascam_imager_readfile`\n\n### Read a single file\n\n```python\n>>> import nascam_imager_readfile\n>>> filename = "path/to/data/2020/01/01/atha_nascam02/ut06/20200101_0600_atha_nascam02_full.pgm.gz"\n>>> img, meta, problematic_files = nascam_imager_readfile.read(filename)\n```\n\n### Read multiple files\n\n```python\n>>> import nascam_imager_readfile, glob\n>>> file_list = glob.glob("path/to/files/2020/01/01/atha_nascam02/ut06/*full.pgm*")\n>>> img, meta, problematic_files = nascam_imager_readfile.read(file_list)\n```\n\n### Read using multiple worker processes\n\n```python\n>>> import nascam_imager_readfile, glob\n>>> file_list = glob.glob("path/to/files/2020/01/01/atha_nascam02/ut06/*full.pgm*")\n>>> img, meta, problematic_files = nascam_imager_readfile.read(file_list, workers=4)\n```\n\n## Development\n\nClone the repository and install dependencies using Poetry.\n\n```console\n$ git clone https://github.com/ucalgary-aurora/nascam-imager-readfile.git\n$ cd nascam-imager-readfile/python\n$ make install\n```\n\n## Testing\n\n```console\n$ make test\n[ or do each test separately ]\n$ make test-flake8\n$ make test-pylint\n$ make test-pytest\n```\n',
    'author': 'Darren Chaddock',
    'author_email': 'dchaddoc@ucalgary.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ucalgary-aurora/nascam-imager-readfile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
