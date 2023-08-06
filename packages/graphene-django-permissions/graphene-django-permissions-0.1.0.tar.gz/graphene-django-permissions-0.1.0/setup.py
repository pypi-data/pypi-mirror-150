# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_django_permissions', 'tests', 'tests.migrations']

package_data = \
{'': ['*']}

install_requires = \
['graphene-django>=2.15.0,<3.0.0']

setup_kwargs = {
    'name': 'graphene-django-permissions',
    'version': '0.1.0',
    'description': 'A performant holistic permissions layer for graphene-django/GraphQL.',
    'long_description': '# Graphene Django Permissions\n\n[![pypi](https://img.shields.io/pypi/v/graphene-django-permissions.svg)](https://pypi.org/project/graphene-django-permissions/)\n[![python](https://img.shields.io/pypi/pyversions/graphene-django-permissions.svg)](https://pypi.org/project/graphene-django-permissions/)\n[![Build Status](https://github.com/sjdemartini/graphene-django-permissions/actions/workflows/dev.yml/badge.svg)](https://github.com/sjdemartini/graphene-django-permissions/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/sjdemartini/graphene-django-permissions/branch/main/graphs/badge.svg)](https://codecov.io/github/sjdemartini/graphene-django-permissions)\n\nA performant, holistic permissions layer for graphene-django/GraphQL.\n',
    'author': 'Steven DeMartini',
    'author_email': 'sjdemartini@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sjdemartini/graphene-django-permissions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
