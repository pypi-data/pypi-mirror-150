from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A chat client that connects to Chat Connector Network.'

setup(
    name="ChatConnector",
    version=VERSION,
    author="TheShulkerBox",
    author_email="<shivek.sethi.saraf@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame', 'easygui'],
    keywords=['python', 'chat client', 'chat connector', 'chat', 'sockets'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Telecommunications Industry",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
