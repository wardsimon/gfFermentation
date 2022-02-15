from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='gfConical',
    version='v0.0.2',
    packages=['gfConical'],
    url='https://github.com/wardsimon/gfConical/',
    license='BSD3',
    author='simonward',
    author_email='',
    description='Connect and control the Grainfather conical fermenter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[requests]
)
