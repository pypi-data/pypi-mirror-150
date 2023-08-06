from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1a1'
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
    package_dir={"src": "src"},
    install_requires=[
        "typer==0.4.1"
    ],
    keywords=['python', 'memory-forward'],
    classifiers=[
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
