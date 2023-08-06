# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wiktrola']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'gTTS>=2.2.4,<3.0.0',
 'rich-click>=1.3.0,<2.0.0',
 'wikipedia>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['pyKaraoke = wiktrola.script:run']}

setup_kwargs = {
    'name': 'wiktrola',
    'version': '1.0.1',
    'description': 'Transform any Wikipedia article into an MP3',
    'long_description': '# wiktrola\nTransform any Wikipedia page into an MP3 file!\n\n## Installing the bot\nTo install the bot there are a few simple steps:\n#### Ubuntu Linux \n##### The following instructions are based on Windows WSL2 and Ubuntu however any flavour of Linux will work with possibly slightly different commands.\n\n##### Confirm Python 3 is installed\n\n#####\n```console\n\n$ python3 -V\nPython 3.9.10\n\n```\n\n##### Create and activate a virtual environment\n\n######\n```console\n\n$ sudo apt install python3-venv\n$ python3 -m venv wiktrola\n$ source wiktrola/bin/activate\n(wiktrola)$\n\n```\n##### Install the bot\n```console\n\n(message_room)$pip install wiktrola\n\n```\n### Windows\n\n#### [Download Python](https://python.org)\n#### Create and activate a virtual environment\n#####\n```console\n\nC:\\>python3 -m venv wiktrola\nC:\\>wiktrola\\Scripts\\activate\n(wiktrola) C:\\>\n\n```\n#### Install the requirements\n```console\n\n(message_room)$pip install wiktrola\n\n```\n\n## Using the bot\n### Run the bot as an interactive session\n```console\n\n(wiktrola)$ wiktrola\n\n```\n### The form questions:\n\n##### Question 1 - What is the title of the Wikipedia page you want to convert?\n\n### The bot will then display all Wikipeida pages related to that title.\n\n### If your title matches a page in the list, the bot will then create an audio file for that page.\n\n### Be patient as the bot may take a while to create the audio file.\n\n### The audio file will open in your browser',
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
