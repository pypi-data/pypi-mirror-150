# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shapes']

package_data = \
{'': ['*']}

install_requires = \
['dotmap>=1.3.30,<2.0.0',
 'imutils>=0.5.4,<0.6.0',
 'numpy>=1.22.3,<2.0.0',
 'opencv-python>=4.5.5,<5.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'shaapes',
    'version': '0.1.0.dev8',
    'description': 'A graphical shape based esolang',
    'long_description': '![A pseudo-quine](https://raw.githubusercontent.com/photon-niko/shapes/main/logo/Shapes.png "A pseudo-quine")\n\n# Shapes!\n\nShapes is a~~n award winning~~ graphical esolang that uses images with shapes!\n\n## Shapes‽\n\nIn short, a Shapes program consists of shapes and paths connecting them. Each shape does different things depending on the shape of the shape.\n\nFor more Shapes Information, go to the [wiki](https://github.com/PhotonNikko/shapes/wiki).\n\n## Shapes?\n\n> How to Shapes?????\n\n### PIP\n\n* Make sure `pip` is up-to-date.\n  ```\n  python -m pip install pip --upgrade\n  ```\n* It\'s shaapes with 2 As\n  ```\n  python -m pip install shaapes\n  ```\n* Interpret Shapes programs with \n  ```\n  python -m shapes interpret "path\\to\\program.png"\n  ```\n* For more options and or thingies, do\n  ```\n  python -m shapes --help\n  ```\n## Shapes!!!\nHello, World!\n![](https://raw.githubusercontent.com/photon-niko/shapes/main/examples/helloworld.png)\n\nTruth machine\n![](https://raw.githubusercontent.com/photon-niko/shapes/main/examples/truth-machine.png)\n\n[more...](https://github.com/photon-niko/shapes/tree/main/examples)\n\n## Shapes...\n\nSoon™:\n* ~~Better docs~~\n* Better shape classification\n* Functionoid path enviornments\n* [...](https://github.com/photon-niko/shapes/blob/main/roadmap.md)\n\n## Shapes...?\n\n[Consider contributing to Shapes!](https://github.com/photon-niko/shapes/blob/main/CONTRIBUTING.md)\n\n-------\n\n> Star this repo if you like my esolang :)\n',
    'author': 'Calico Niko',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/photon-niko/shapes/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '<3.11',
}


setup(**setup_kwargs)
