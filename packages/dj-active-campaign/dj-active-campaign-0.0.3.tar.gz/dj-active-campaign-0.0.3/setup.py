# --------------------------------------------
# Copyright 2022, Roberto Himmelbauer Perches
# @Author: Roberto Himmelbauer Perches
# @Date:   2022-4-28 09:50:49
# --------------------------------------------

from os import path
from setuptools import setup, find_packages

from dj_active_campaign.__version__ import VERSION

file_path = path.abspath(path.dirname(__file__))
with open(path.join(file_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

package_metadata = {
    'name': 'dj-active-campaign',
    'version': VERSION,
    'description': 'A Django Implementation of the Active Campaign Python SDK',
    'long_description': long_description,
    'url': 'https://github.com/rhimmelbauer/django-active-campaign',
    'author': 'Roberto Himmelbauer Perches',
    'author_email': 'robertoh89@gmail.com',
    'license': '',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
    ],
}

setup(
    **package_metadata,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "Django>=3,<4.0",
        "django-autoslug",
        "django-site-configs",
        "django-integrations"
        ],
    extras_require={
        'dev': [
            'dj-database-url',
            'psycopg2-binary',
            'django-allauth',
            'django-crispy-forms'
        ],
        'test': [],
        'prod': [],
        'build': [
            'setuptools',
            'wheel',
            'twine',
            ],
        'docs': [
            'coverage==4.4.1',
            'Sphinx==1.6.4'
            ],
    }
)