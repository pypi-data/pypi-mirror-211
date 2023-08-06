from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.0'
DESCRIPTION = 'Python GUIs made easy'

# Setting up
setup(
    name="PyOptionPane",
    version=VERSION,
    author="yavda1",
    author_email="<yavda1@courvix.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['tk', 'Pillow'],
    keywords=['python', 'tkinter', 'gui', 'JOptionPane'],
    classifiers=[

        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)