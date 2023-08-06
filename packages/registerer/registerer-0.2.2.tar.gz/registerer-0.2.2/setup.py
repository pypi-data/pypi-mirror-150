# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['registerer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'registerer',
    'version': '0.2.2',
    'description': 'Everything you need to implement maintainable and easy to use registry patterns in your project.',
    'long_description': '# Fast Registry\n[![](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)\n[![](https://github.com/danialkeimasi/python-registerer/workflows/tests/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)\n[![](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)\n\nEverything you need to implement maintainable and easy to use registry patterns in your project.\n# Installation\n\n```sh\npip install registerer\n```\n\n# Register Classes\nRegister classes with the same interface, enforce the type check and enjoy the benefits of type hints:\n```py\nfrom registerer import Registerer\n\n\nclass Animal:\n    def talk(self) -> None:\n        raise NotImplementedError\n\n\n# create a registry that requires registered items to implement the Animal interface:\nanimal_registry = Registerer(Animal)\n\n\n@animal_registry.register("dog")\nclass Dog(Animal):\n    def talk(self) -> None:\n        return "woof"\n```\n\n\n# Register Functions\nRegister functions and benefit from the function annotations validator (optional):\n```py\nfrom registerer import Registerer, FunctionAnnotationValidator\n\ndatabase_registry = Registerer(\n    validators=[\n        FunctionAnnotationValidator(annotations=[("name", str)]),\n    ]\n)\n\n@database_registry.register("sqlite")\ndef sqlite_database_connection(name: str):\n    return f"sqlite connection {name}"\n\n```\n\n# Create Custom Validators\nBy Creating a subclass of `RegistryValidator`, you can create your own validators to check registered classes/functions if you need to.\n\n# Examples\n- [Class - Simple Type Checking](https://github.com/danialkeimasi/python-registerer/blob/main/examples/class.py)\n- [Class - Custom Validator](https://github.com/danialkeimasi/python-registerer/blob/main/examples/class-with-custom-validator.py)\n- [Function - Simple](https://github.com/danialkeimasi/python-registerer/blob/main/examples/function.py)\n- [Function - With Type Annotation Validator](https://github.com/danialkeimasi/python-registerer/blob/main/examples/function-with-validator.py)\n',
    'author': 'Danial Keimasi',
    'author_email': 'danialkeimasi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danialkeimasi/python-registerer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
