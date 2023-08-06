from setuptools import setup, find_packages

VERSION = '0.1.4'
DESCRIPTION = 'A python package for testing strategies'
LONG_DESCRIPTION = 'A python package for testing strategies in the context of a trading strategy framework and calculating the performance of the strategy.'
with open("strategy_tester/requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()
    
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "strategy_tester/README.md").read_text()

# Setting up
setup(
    name="strategy_tester",
    version=VERSION,
    author="Ali Ardakani",
    author_email="aliardakani78@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    keywords=['python', 'strategy', 'tester', 'trading', 'backtesting', 'performance'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)