# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpleini']

package_data = \
{'': ['*'], 'simpleini': ['.idea/*', '.idea/inspectionProfiles/*']}

entry_points = \
{'console_scripts': ['APPLICATION-NAME = __init__:main']}

setup_kwargs = {
    'name': 'simpleini',
    'version': '0.1.8',
    'description': 'Simple use ini files',
    'long_description': "This is the simplest way to interact with a single ini file to store settings. \n\nAttention! It is delivered together with logging to a file. You need to try to understand.\n\n#### Use:\n```python\n\tfrom simpleini import SETTINGS, logging\n\n\tparsed_data = SETTINGS(<names_settings>, <required_settings>)\n\n\t# names_settings - A string with the names of the settings stored in the file. If there is no file, it will be created and the program will be completed.\n\t# required_settings - comma-separated list of required variables. 'all' - to check all variables\n```python\n\n\n#### Example ini reader (simple mode):\n```python\n# Read from [DEFAULT] section\n\tparsed_data = SETTINGS('settings1, settings2, settings3', 'all')\n\n\tsettings1 = parsed_data.settings1\n\tsettings2 = parsed_data.settings2\n\tsettings3 = parsed_data.settings3\n```python\n\n#### Examle ini readred\n```python\nparsed_data = SETTINGS()\nsettings1 = parsed_data.section_name.settings1\nsettings2 = parsed_data.section_name.settings2\nsettings3 = parsed_data.section_name_2.settings1\n```python\n\n#### Example with required fields\n```python\nsettings = SETTINGS(required_fields='NEW_DEFAULT.path_default')\n```python\n\n#### Example set\n```python\nsettings.set('test.one', 123)\n```python\n\n#### Example remove section\n```python\nsettings.remove('section_name')\n```python\n\n#### Example remove option\n```python\nsettings.remove('section_name.option_name')\n```python\n\n#### Example logging:\n```python\n\tlogging('message for log') # it will write a file to the project folder log.txt and it will add incoming information to it\n```python\n",
    'author': 'to101',
    'author_email': 'to101kv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
