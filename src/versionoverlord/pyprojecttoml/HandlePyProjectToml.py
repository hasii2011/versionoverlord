
from typing import cast

from logging import Logger
from logging import getLogger

from os import sep as osSep

from pathlib import Path

from re import search as regExSearch
from re import sub as regExSub
from re import Match

from versionoverlord.IHandler import IHandler

from versionoverlord.Common import PYPROJECT_TOML
from versionoverlord.Common import Packages
from versionoverlord.Common import UpdatePackage


class HandlePyProjectToml(IHandler):
    """
    Handles the pyproject.toml file
    """

    def __init__(self, packages: Packages):
        self.logger: Logger = getLogger(__name__)
        super().__init__(packages)

        self._pyProjectToml: Path = Path(f'{self._projectsBase}{osSep}{self._projectDirectory}{osSep}{PYPROJECT_TOML}')

    @property
    def configurationExists(self) -> bool:
        """
        Returns:  'True' if the project has this type of configuration file, else 'False'
        """
        return self._pyProjectToml.exists()

    def update(self):

        """
        Updates a project's pyproject.toml  Updates the "dependencies" section
        """
        pyProjectToml = self._pyProjectToml

        with open(pyProjectToml, 'rt') as inputFd:
            content: str = inputFd.read()

        assert inputFd.closed, 'Should be auto closed'
        self.logger.info(f'{content=}')

        updatedContent: str = self._updateDependencies(content)
        self.logger.info(f'{updatedContent=}')

        with open(pyProjectToml, 'wt') as outputFd:
            outputFd.write(updatedContent)

        assert inputFd.closed, 'Should be auto closed'

    def _updateDependencies(self, fileContent: str) -> str:
        """
        This works with style requirements.txt, setup.py & pyproject.toml

        Rationale:  These files are typically not large;  So let's process everything in
        memory

        Args:
            fileContent:  The entire file contents

        Returns:  The updated file content
        """

        for pkg in self._packages:
            package: UpdatePackage = cast(UpdatePackage, pkg)

            oldDependency: str = f'{package.packageName}=={package.oldVersion}'
            newDependency: str = f'{package.packageName}=={package.newVersion}'

            match: Match | None = regExSearch(pattern=oldDependency, string=fileContent)
            if match is None:
                oldDependency = f'{package.packageName}~={package.oldVersion}'
                newDependency = f'{package.packageName}~={package.newVersion}'

                match = regExSearch(oldDependency, fileContent)
                assert match, 'Secondary package string must match'
                fileContent = regExSub(pattern=oldDependency, repl=newDependency, string=fileContent)

            else:
                fileContent = regExSub(pattern=oldDependency, repl=newDependency, string=fileContent)

            assert match, 'We should only come here with valid package names'

        return fileContent
