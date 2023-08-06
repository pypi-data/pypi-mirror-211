#!/usr/bin/env python

"""The setup script."""

import re
from setuptools import setup, find_packages


def get_long_description():
    return "See https://github.com/Nanguage/mrbios"


def get_version():
    with open("mrbios/__init__.py") as f:
        for line in f.readlines():
            m = re.match("__version__ = '([^']+)'", line)
            if m:
                return m.group(1)
        raise IOError("Version information can not found.")


def get_requirements_from_file(filename):
    requirements = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            if line and not line.startswith('#'):
                requirements.append(line)
    return requirements


def get_install_requirements():
    return get_requirements_from_file("requirements.txt")


requires_test = ['pytest', 'pytest-cov', 'flake8', 'mypy']
requires_doc = get_requirements_from_file("docs/requirements.txt")
requires_dev_tools = ["pip", "setuptools", "wheel", "twine", "ipdb"]
requires_type = ["types-PyYAML"]


setup(
    author="Weize Xu",
    author_email='vet.xwz@gmail.com',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
            'mrbios=mrbios.__main__:main',
        ],
    },
    description="A bioinformatics scripts management tool.",
    install_requires=get_install_requirements(),
    license="MIT license",
    long_description=get_long_description(),
    include_package_data=True,
    keywords='mrbios',
    name='mrbios',
    packages=find_packages(include=['mrbios', 'mrbios.*']),
    url='https://github.com/Nanguage/mrbios',
    version=get_version(),
    zip_safe=False,
    extras_require={
        'test': requires_test + requires_type,
        'doc': requires_doc,
        'dev': (
            requires_dev_tools + requires_test +
            requires_doc + requires_type
        ),
    }
)
