from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='md_inputs',
    version='1.1',
    py_modules=['md_inputs'],
    install_requires = ['markdown>=3.0'],
    description='Python-mardown extension for inputs(text, select, checkbox...) in markdown document',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gavin Guo',
    author_email='gghyoo@qq.com',
    url='https://www.python.org/sigs/distutils-sig/'
)