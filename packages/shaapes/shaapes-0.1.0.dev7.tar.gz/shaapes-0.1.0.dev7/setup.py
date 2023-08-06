# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shapes', 'shapes.shapes39']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shaapes',
    'version': '0.1.0.dev7',
    'description': 'A graphical shape based esolang',
    'long_description': '![A pseudo-quine](https://raw.githubusercontent.com/photon-niko/shapes/main/logo/Shapes.png "A pseudo-quine")\n\n# Shapes!\n\nShapes is a~~n award winning~~ graphical esolang that uses images with shapes!\n\n## Shapes‽\n\nIn short, a Shapes program consists of shapes and paths connecting them. Each shape does different things depending on the shape of the shape.\n\nFor more Shapes Information, go to the [wiki](https://github.com/PhotonNikko/shapes/wiki).\n\n## Shapes?\n\n> How to Shapes?????\n\n* Make sure the python version is 3.10 and `pip` is up-to-date.\n>Psst, there is also a [3.9 version of this interpreter](https://github.com/photon-niko/shapes/tree/main/shapes/shapes39) if you just can\'t bother installing 3.10\n* Clone this repo\n>Or clone the [slow branch](https://github.com/photon-niko/shapes/tree/slow) for Slow Shapes™\n* Then, change your directory to wherever this file is located.\n* Install requirements with\n  ```\n  python -m pip install -r requirements.txt\n  ```\n* Interpret Shapes programs with \n  ```\n  python -m shapes interpret "path\\to\\program.png"\n  ```\n> With 3.9, do\n> ```\n> python -m shapes.shapes39 interpret "path\\to\\program.png"\n> ```\n\n* For more options and or thingies, do\n  ```\n  python -m shapes --help\n  ```\n## Shapes!!!\nHello, World!\n![](https://raw.githubusercontent.com/photon-niko/shapes/main/examples/helloworld.png)\n\nTruth machine\n![](https://raw.githubusercontent.com/photon-niko/shapes/main/examples/truth-machine.png)\n\n[more...](https://github.com/photon-niko/shapes/tree/main/examples)\n\n## Shapes...\n\nSoon™:\n* ~~Better docs~~\n* Better shape classification\n* Functionoid path enviornments\n* [...](https://github.com/photon-niko/shapes/blob/main/roadmap.md)\n\n## Shapes...?\n\n[Consider contributing to Shapes!](https://github.com/photon-niko/shapes/blob/main/CONTRIBUTING.md)\n\n-------\n\n> Star this repo if you like my esolang :)\n',
    'author': 'Calico Niko',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/photon-niko/shapes/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
