# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voice_presentation_control']

package_data = \
{'': ['*']}

install_requires = \
['PyAudio>=0.2.11,<0.3.0',
 'PyAutoGUI>=0.9.53,<0.10.0',
 'SpeechRecognition>=3.8.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['vpc = voice_presentation_control.cli:start_cli']}

setup_kwargs = {
    'name': 'voice-presentation-control',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Xyphuz',
    'author_email': 'xyphuzwu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
