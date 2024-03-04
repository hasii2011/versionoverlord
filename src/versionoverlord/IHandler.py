from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from abc import ABC
from abc import abstractmethod

from pathlib import Path

from re import search as regExSearch
from re import sub as regExSub
from re import Match


from versionoverlord.Common import Packages
from versionoverlord.Common import UpdatePackage

from versionoverlord.EnvironmentBase import EnvironmentBase

EQUAL_EQUAL:           str = '=='
APPROXIMATELY_EQUAL:   str = '~='
GREATER_THAN_OR_EQUAL: str = '>='
LESS_THAN_OR_EQUAL:    str = '<='
GREATER_THAN:          str = '>'
LESS_THAN:             str = '<'

MATCH_PATTERNS: List[str] = [
    EQUAL_EQUAL, APPROXIMATELY_EQUAL, GREATER_THAN_OR_EQUAL, LESS_THAN_OR_EQUAL, GREATER_THAN, LESS_THAN
]


class IHandler(ABC, EnvironmentBase):
    """
    Interface that configuration handlers must implement

    """
    def __init__(self, packages: Packages):

        self._packages:  Packages = packages
        self.baseLogger: Logger   = getLogger(__name__)

        super().__init__()

    @abstractmethod
    def update(self):
        """
        Updates a project's file.
        """
        pass

    @property
    @abstractmethod
    def configurationExists(self) -> bool:
        """
        Returns:  'True' if the project has this type of configuration file, else 'False'
        """
        return True

    def _update(self, configurationFilePath: Path):

        """
        Updates a project configuration file
        """
        pyProjectToml = configurationFilePath

        with open(pyProjectToml, 'rt') as inputFd:
            content: str = inputFd.read()

        assert inputFd.closed, 'Should be auto closed'
        self.baseLogger.info(f'{content=}')

        updatedContent: str = IHandler.updateDependencies(content, self._packages)
        self.baseLogger.info(f'{updatedContent=}')

        with open(pyProjectToml, 'wt') as outputFd:
            outputFd.write(updatedContent)

        assert inputFd.closed, 'Should be auto closed'

    @classmethod
    def updateDependencies(cls, fileContent: str, packages: Packages) -> str:
        """
        This works with style requirements.txt, setup.py & pyproject.toml

        Rationale:  These files are typically not large;  So let's process everything in
        memory

        Args:
            fileContent:  The entire file contents
            packages:     The packages to update in the file content

        Returns:  The updated file content
        """

        for pkg in packages:
            package: UpdatePackage = cast(UpdatePackage, pkg)

            match: Match | None = None
            for matchPattern in MATCH_PATTERNS:
                oldDependency: str = f'{package.packageName}{matchPattern}{package.oldVersion}'
                newDependency: str = f'{package.packageName}{matchPattern}{package.newVersion}'

                match = regExSearch(pattern=oldDependency, string=fileContent)
                if match is None:
                    continue
                else:
                    fileContent = regExSub(pattern=oldDependency, repl=newDependency, string=fileContent)
                    break

            assert match is not None, 'We should only come here with valid package names'

            # oldDependency: str = f'{package.packageName}=={package.oldVersion}'
            # newDependency: str = f'{package.packageName}=={package.newVersion}'
            #
            # match: Match | None = regExSearch(pattern=oldDependency, string=fileContent)
            # if match is None:
            #     oldDependency = f'{package.packageName}~={package.oldVersion}'
            #     newDependency = f'{package.packageName}~={package.newVersion}'
            #
            #     match = regExSearch(oldDependency, fileContent)
            #     assert match, 'Secondary package string must match'
            #     fileContent = regExSub(pattern=oldDependency, repl=newDependency, string=fileContent)
            #
            # else:
            #     fileContent = regExSub(pattern=oldDependency, repl=newDependency, string=fileContent)
            #
            # assert match, 'We should only come here with valid package names'

        return fileContent
