import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="OverLordUnitTest",
    version="1.0.0",
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='A Bogus Unit Test project',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/OverLordUnitTest",
    packages=[
        'overlordunitttest'
    ],
    package_data={
        'overlordunitttest': ['py.typed'],
    },

    install_requires=['ogl==0.80.0', 'untangle==1.3.0'],
)
