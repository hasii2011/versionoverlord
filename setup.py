import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="versionoverlord",
    version="0.1.0",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Dependency Manager',
    long_description=README,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url="https://github.com/versionoverlord",
    packages=[
        'versionoverlord'
    ],
    install_requires=[
        'click~=8.1.3',
        'hasiicommon~=0.1.0',
    ],
    entry_points='''
        [console_scripts]
        versionoverlord=versionoverlord.VersionOverlord:commandHandler
    ''',
)
