from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Quran SBU All'
LONG_DESCRIPTION = 'First Python Package'

# Setting up
setup(
    name="quranallsbuforuni",
    version=VERSION,
    author="Masoud Shafiei",
    author_email="masoudshafiei89@yahoo.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['quran', 'sbu'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)