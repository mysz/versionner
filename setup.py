from setuptools import setup, find_packages
from codecs import open
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))

with open(path.join(BASE_DIR, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='versionner',
    version='0.4.3',
    description='versionner helps manipulating version of the project.',
    long_description=long_description,
    url='http://mysz.github.io/versionner/',
    author='Marcin Sztolcman',
    author_email='marcin@urzenia.net',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['argparse', 'semver'],
    py_modules=['versionner'],

    keywords='version management',

    entry_points={
        'console_scripts': [
            'versionner=versionner:main',
        ],
    },
)

