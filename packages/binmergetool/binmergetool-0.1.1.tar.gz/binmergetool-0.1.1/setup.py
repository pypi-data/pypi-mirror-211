# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['binmergetool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'binmergetool',
    'version': '0.1.1',
    'description': 'Tool for merging binary files together',
    'long_description': "# binmergetool\nSimple tool for merging two binary files together.\n\n# Install\n\n    pip install binmergetool\n\n# Usage\n\n## Example: merging Arduino bootloader with application code\n\nIn this example, we'll add the Arduino bootloader to a compiled binary file for one-step flashing of microcontrollers.\nApplication code starts at 0x2000 so we set this as the offset.\n\n    python -m binmergetool bootloader.bin application.bin 0x2000 0xFF application_with_bootloader.bin\n\n",
    'author': 'Antoine Jeanson',
    'author_email': 'anonymous@mail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/antoinejeanson/binmergetool',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
