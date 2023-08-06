# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyeph',
 'pyeph.calc',
 'pyeph.calc.labor_market',
 'pyeph.calc.poverty',
 'pyeph.calc.template',
 'pyeph.get',
 'pyeph.get.basket',
 'pyeph.get.equivalent_adult',
 'pyeph.get.mautic',
 'pyeph.get.microdata',
 'pyeph.tools']

package_data = \
{'': ['*'], 'pyeph': ['.files/*'], 'pyeph.tools': ['.examples/*']}

install_requires = \
['ipykernel>=6.13.0,<7.0.0', 'pandas>=1.1.5,<2.0.0', 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'pyeph',
    'version': '1.1.5',
    'description': "PyEPH es una librería para el procesamiento de la Encuesta Permanente de Hogares (eph) en Python. Permite la descarga de archivos de EPH's y otros como la canasta basica y adulto equivalente , como asi también algunos calculos rápidos relacionados con las mismas",
    'long_description': None,
    'author': 'Maria Carolina Trogliero, Mariano Valdez Anopa, Maria Gaska',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
