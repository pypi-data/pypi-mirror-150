# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongoengine_dsl', 'mongoengine_dsl.lexer', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['antlr4-python3-runtime>=4.10,<5.0', 'mongoengine>=0,<1']

extras_require = \
{'dev': ['tox==3.25.0',
         'pre-commit>=2.12.0,<3.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.3.0,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.4.0,<4.0.0',
         'mkdocs-material>=8.2.13,<9.0.0',
         'mkdocstrings[python]>=0.18.1,<0.19.0'],
 'test': ['pytest==6.2.5',
          'pytest-cov==2.10.1',
          'black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mongomock==3.23.0']}

setup_kwargs = {
    'name': 'mongoengine-dsl',
    'version': '0.1.5',
    'description': 'DSL to MongoEngine Q.',
    'long_description': '<center>\n\n![Logo](docs/assets/logo.png)\n\n<a href="https://pypi.python.org/pypi/mongoengine_dsl">\n    <img src="https://img.shields.io/pypi/v/mongoengine_dsl.svg" alt="Release Status">\n</a>\n\nDSL to MongoEngine Q\n\n</center>\n\n<!--intro-start-->\n\n## Features\n\n* Build your mongoengine query from DSL syntax\n* Convert your data at build time via transform hook\n\n## Quickstart\n\nInstall\n\n```bash\npip install mongoengine_dsl\n```\n\nUse\n\n```python\nfrom mongoengine import Document, StringField\nfrom mongoengine_dsl import Query\n\n\nclass User(Document):\n    fullname = StringField()\n\n\nUser(fullname="Tom").save()\nUser(fullname="Dick").save()\nUser(fullname="Harry").save()\n\nassert User.objects(\n    Query("fullname: Dick")\n).first().fullname == "Dick"\n\nassert User.objects(\n    Query("fullname: dick", transform={\n        "fullname": lambda x: x.title()\n    })\n).first().fullname == "Dick"\n```\n\n<!--intro-end-->\n\n## More\nFull Documentation: <https://stonemoe.github.io/mongoengine_dsl>\n',
    'author': 'Lake Chan',
    'author_email': 'lakechan96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/StoneMoe/mongoengine_dsl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
