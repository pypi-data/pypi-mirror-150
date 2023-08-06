# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyKaraoke']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'gTTS>=2.2.4,<3.0.0',
 'pymusixmatch>=0.3,<0.4',
 'rich-click>=1.3.0,<2.0.0',
 'rich>=12.4.1,<13.0.0']

entry_points = \
{'console_scripts': ['pyKaraoke = pyKaraoke.script:run']}

setup_kwargs = {
    'name': 'pykaraoke',
    'version': '1.0.1',
    'description': 'A bot that uses the musixmatch API to transform songs into Google Text-to-Speech',
    'long_description': '# pyKaraoke - Use the musixmatch API to transform songs into Google Text-to-Speech\n\n## Getting Started with karegoogle\n\n### Get a Developer Account on MusixMatch\nhttps://developer.musixmatch.com/\n### Get an API Key\n\n### Installing the bot\nTo install the bot there are a few simple steps:\n#### Setup a virtual environment\n##### Ubuntu Linux \n###### The following instructions are based on Windows WSL2 and Ubuntu however any flavour of Linux will work with possibly slightly different commands.\n\n##### Confirm Python 3 is installed\n\n#####\n```console\n\n$ python3 -V\nPython 3.9.10\n\n```\n\n##### Create and activate a virtual environment\n\n#####\n```console\n\n$ sudo apt install python3-venv\n$ python3 -m venv karaoke\n$ source karaoke/bin/activate\n(karaoke)$\n\n```\n#### Install the bot\n```console\n\n(message_room)$pip install pykaraoke\n\n```\n### Windows\n\n#### Confirm Python 3.9 is installed\n##### [Download Python](https://python.org)\n#### Create and activate a virtual environment\n#####\n```console\n\nC:\\>python3 -m venv karaoke\nC:\\>karaoke\\Scripts\\activate\n(pykaraoke) C:\\>\n\n```\n#### Install the requirements\n```console\n\n(message_room)$pip install pykaraoke\n\n```\n\n### Using the bot\n#### Run the bot as an interactive session\n```console\n\n(karaoke)$ pykaraoke\n\n```\n#### The form questions:\n\n##### Question 1 - API Token\n\n##### Question 2 - Arist Name\n\n##### Question 3 - Song Title\n\n\n#### Environment variables\n\nEvery question can be stored as a variable in the environment. This is useful if you want to reuse the same question in multiple messages.\n\nLinux:\nexport TOKEN=<your token>\nexport ARTIST=<artist name>\nexport SONG=<song title>\n\nWindows:\nset TOKEN=<your token>\nset ARTIST=<artist name>\nset SONG=<song title>',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
