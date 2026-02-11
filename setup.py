# -*- coding: utf-8 -*-
"""Setup module."""
from typing import List
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_requires() -> List[str]:
    """Read requirements.txt."""
    requirements = open("requirements.txt", "r").read()
    return list(filter(lambda x: x != "", requirements.split()))


def read_description() -> str:
    """Read README.md and CHANGELOG.md."""
    try:
        with open("README.md") as r:
            description = "\n"
            description += r.read()
        with open("CHANGELOG.md") as c:
            description += "\n"
            description += c.read()
        return description
    except Exception:
        return '''Typio is a lightweight Python library that prints text to the terminal as if it were being typed by a human.
        It supports multiple typing modes (character, word, line, sentence, typewriter, and adaptive),
        configurable delays and jitter for natural variation, and seamless integration with existing code
        via a simple function or a decorator. Typio is designed to be minimal, extensible, and safe,
        making it ideal for demos, CLIs, tutorials, and storytelling in the terminal.'''


setup(
    name='typio',
    packages=['typio'],
    version='0.3',
    description='Typio: Make Your Terminal Type Like a Human',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='Sepand Haghighi',
    author_email='me@sepand.tech',
    url='https://github.com/sepandhaghighi/typio',
    download_url='https://github.com/sepandhaghighi/typio/tarball/v0.3',
    keywords="terminal cli typing typewriter typing-effect console stdout ux",
    project_urls={
        'Source': 'https://github.com/sepandhaghighi/typio'
    },
    install_requires=get_requires(),
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Terminals',
    ],
    license='MIT',
)
