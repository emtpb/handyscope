from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as readme_file:
    long_description = readme_file.read()

setup(
    name='tiepie',

    description='TiePie provides a Python interface to the mobile USB-oscilloscopes made by TiePie.',
    long_description=long_description,

    url='http://emt.uni-paderborn.de',
    author='Tim Hetkaemper',
    author_email='timh1@mail.uni-paderborn.de',
    license='Proprietary',

    # Automatically generate version number from git tags
    use_scm_version=True,

    packages=[
        'tiepie'
    ],

    # Additional data
    package_data={
        'tiepie': ['bin/libtiepie.dll'],
    },

    # Runtime dependencies
    install_requires=[
    ],

    # Setup/build dependencies; setuptools_scm required for git-based versioning
    setup_requires=['setuptools_scm', 'pytest-runner'],

    # Test dependencies
    tests_require=['pytest'],

    # For a list of valid classifiers, see
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers for full list.
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)
