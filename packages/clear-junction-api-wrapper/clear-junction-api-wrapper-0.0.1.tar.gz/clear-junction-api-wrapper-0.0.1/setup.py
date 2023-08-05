from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Clear Junction API Wrapper'
LONG_DESCRIPTION = 'A Python wrapper for the Clear Junction API.'

# Setting up
setup(
    name="clear-junction-api-wrapper",
    version=VERSION,
    author="Richard",
    author_email="<rich_swainson@hotmail.co.uk>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'pytz'],
    keywords=['clear junction', 'api', 'wrapper', 'payment', 'fintech'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
