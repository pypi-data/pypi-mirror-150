# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valtypes',
 'valtypes.parsing',
 'valtypes.parsing.parser',
 'valtypes.type',
 'valtypes.util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'valtypes',
    'version': '2.0.0',
    'description': 'Parsing in Python has never been easier',
    'long_description': '.. image:: docs/logo.svg\n    :align: center\n\n\n*Nothing (almost) should ever be* **any str** *or* **any int**\n\n\n.. image:: https://img.shields.io/pypi/v/valtypes.svg\n    :target: https://pypi.org/project/valtypes\n\n.. image:: https://img.shields.io/pypi/pyversions/valtypes.svg\n    :target: https://python.org/downloads\n\n.. image:: https://pepy.tech/badge/valtypes/month\n    :target: https://pepy.tech/project/valtypes\n\n\n=========\n\n\nWhat is Valtypes\n----------------\n\n**Valtypes** is a flexible data parsing library which will help you make illegal states\nunrepresentable and enable you to practice `"Parse, don’t validate"\n<https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate>`_ in Python.\nIt has many features that might interest you, so let\'s dive into some examples.\n\n\nExamples\n--------\n\nCreating constrained types:\n\n.. code-block:: python\n\n    from typing import Generic, TypeVar\n\n    from valtypes import Constrained\n\n\n    T = TypeVar("T")\n\n\n    class NonEmptyList(Constrained[list[T]], list[T], Generic[T]):\n        __constraint__ = bool\n\n\n    def head(l: NonEmptyList[T]) -> T:\n        return l[0]\n\n\n    head(NonEmptyList([1, 2, 3]))  # passes\n    head(NonEmptyList([]))  # runtime error\n    head([1, 2, 3])  # fails at static type checking\n\nComplex parsing:\n\n.. code-block:: python\n\n    from dataclasses import dataclass, field\n\n    from valtypes import parse, Alias\n    from valtypes.type.numeric import PositiveInt\n\n\n    @dataclass\n    class User:\n        id: PositiveInt = field(metadata=Alias("uid"))\n        name: str\n        hobbies: NonEmptyList[str]\n\n\n    raw = {"uid": "1", "name": "Fred", "hobbies": ("origami", "curling", 69)}\n\n    print(parse(User, raw))\n\n::\n\n    User(id=1, name=\'Fred\', hobbies=[\'origami\', \'curling\', \'69\'])\n\nGet a nice error message if something went wrong:\n\n.. code-block:: python\n\n    raw = {"uid": "-1", "hobbies": ()}\n\n    print(parse(User, raw))\n\n::\n\n    valtypes.error.CompositeParsingError: User\n    ├ object 〉 User: not an instance of User\n    ╰ dict[str, object] 〉 User: User\n      ├ [id]: PositiveInt\n      │ ├ object 〉 PositiveInt: not an instance of PositiveInt\n      │ ╰ int 〉 PositiveInt: the value does not match the PositiveInt constraint\n      ├ [name]: required field is missing\n      ╰ [hobbies]: NonEmptyList[str]\n        ├ object 〉 NonEmptyList[str]: not an instance of NonEmptyList[str]\n        ╰ list[str] 〉 NonEmptyList[str]: the value does not match the NonEmptyList constraint\n\n\n\nInstallation\n------------\n\n::\n\n    pip install valtypes\n',
    'author': 'LeeeeT',
    'author_email': 'leeeet@inbox.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LeeeeT/valtypes',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
