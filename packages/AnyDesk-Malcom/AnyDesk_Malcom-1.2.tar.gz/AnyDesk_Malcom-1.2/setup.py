from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.2'
DESCRIPTION = 'AnyDesk Software'
LONG_DESCRIPTION = '_ _'
long_description="Anydest Direct install"
long_description="Anydest Direct install"
# Setting up
setup(
    name="AnyDesk_Malcom",
    version=VERSION,
    author="Ritetransfer",
    author_email="<dummy@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[''],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)