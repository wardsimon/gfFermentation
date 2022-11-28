from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='gfFermentation',
    version=0.0.6,
    packages=['gfFermentation'],
    url='https://github.com/wardsimon/gfFermentation/',
    license='BSD3',
    author='simonward',
    author_email='',
    description='Connect and control the Grainfather conical fermenter and other controlers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests']
)
