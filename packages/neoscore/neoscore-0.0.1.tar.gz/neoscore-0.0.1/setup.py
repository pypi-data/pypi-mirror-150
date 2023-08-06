# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neoscore',
 'neoscore.core',
 'neoscore.interface',
 'neoscore.interface.qt',
 'neoscore.western']

package_data = \
{'': ['*'],
 'neoscore': ['resources/*',
              'resources/fonts/bravura/*',
              'resources/fonts/lora/*',
              'resources/smufl/*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0', 'img2pdf==0.4.3', 'sortedcontainers==2.4.0']

setup_kwargs = {
    'name': 'neoscore',
    'version': '0.0.1',
    'description': 'A graphical musical notation library',
    'long_description': '# neoscore\n\n## *notation without bars*\n\n![A score with colored blocks and squiggly lines](/gallery/promo_image.png)\n*[Example source](/examples/promo_image.py)*\n\nNeoscore is a Python library for creating scores without limits. While other notation software assumes scores follow a narrow set of rules, neoscore treats scores as shapes and text with as few assumptions as possible. In neoscore, staves and noteheads are just one way of writing. Its programmatic nature makes it especially useful for generative scoremaking, and it even supports experimental animation and live-coding!\n\n## Quick Start\n\nYou can install neoscore with pip using `pip install neoscore`, after which you should be able to run this example:\n\n```python\nfrom neoscore.common import *\nneoscore.setup()\nText(ORIGIN, None, "Hello, neoscore!")\nneoscore.show()\n```\n\n## Documentation\n\nVisit [neoscore.org](https://neoscore.org) for thorough documentation and dozens of examples. You can find more [elaborate examples in this repository here](/examples).\n\n',
    'author': 'Andrew Yoon',
    'author_email': 'andrew@nothing-to-say.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://neoscore.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
