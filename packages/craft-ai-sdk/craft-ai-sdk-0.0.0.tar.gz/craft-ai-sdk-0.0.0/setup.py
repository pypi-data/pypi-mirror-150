# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['craft_ai_sdk']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['format = scripts:format',
                     'lint = scripts:lint',
                     'reformat = scripts:reformat',
                     'test = scripts:test',
                     'test-base = scripts:test_base',
                     'test-platform = scripts:test_platform']}

setup_kwargs = {
    'name': 'craft-ai-sdk',
    'version': '0.0.0',
    'description': 'Craft.AI – MLOps platform',
    'long_description': '# Craft.AI Python SDK\n\nThis Python SDK lets you interact with Craft.AI MLOps Platform.\n',
    'author': 'craft ai',
    'author_email': 'contat@craft.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.craft.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
