from setuptools import find_packages, setup

import os

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1a8'
DESCRIPTION = 'A CLI tool for batch editing files'
LONG_DESCRIPTION = 'A CLI tool developed for memory forward to help batch edit files, and their metadata.'

# Setting up
setup(
    name="memory-forward",
    version=VERSION,
    author="Justin Robertson",
    author_email="justin.robertson@auctane.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["typer==0.4.1"],
    python_requires=">=3.9",
    keywords=['python', 'memory-forward'],
    classifiers=[
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points = '''
        [console_scripts]
        memory-forward=memory_forward.cli:main
    '''
)
