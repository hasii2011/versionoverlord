
from typing import cast

from logging import Logger
from logging import getLogger

from pathlib import Path

from re import sub as regexSubstitute

from os import sep as osSep

from versionoverlord.Common import SETUP_PY
from versionoverlord.Common import Packages
from versionoverlord.Common import UpdatePackage


from versionoverlord.IHandler import IHandler


class HandleSetupPy(IHandler):
    """
    Handles the setup.py file
    """
    def __init__(self, packages: Packages):

        self.logger: Logger = getLogger(__name__)
        super().__init__(packages)

        self._setupPyPath: Path = Path(f'{self._projectsBase}{osSep}{self._projectDirectory}{osSep}{SETUP_PY}')

    @property
    def configurationExists(self) -> bool:
        return self._setupPyPath.exists()

    def update(self):
        """
        Updates a project's setup.py file.  Updates the "requires"
        """
        setupPyPath: Path = self._setupPyPath

        with open(setupPyPath, 'rt') as inputFd:
            content: str = inputFd.read()

        assert inputFd.closed, 'Should be auto closed'
        self.logger.info(f'{content=}')

        updatedContent: str = self._updateDependencies(content)
        self.logger.info(f'{updatedContent=}')

        with open(setupPyPath, 'wt') as outputFd:
            outputFd.write(updatedContent)

        assert inputFd.closed, 'Should be auto closed'

    def _updateRequires(self, contentLine: str) -> str:
        """
        Updates the "requires" string
        Handles "==" and "~=" types

        Args:
            contentLine: The line to update

        Returns:  The updated string
        """
        updatedLine: str = contentLine
        for pkg in self._packages:
            package: UpdatePackage = cast(UpdatePackage, pkg)

            equalPrefix:  str = f'{package.packageName}=='
            almostPrefix: str = f'{package.packageName}~='

            equalPattern:  str = f'{equalPrefix}{str(package.oldVersion)}'
            almostPattern: str = f'{almostPrefix}{str(package.oldVersion)}'
            repl:          str = f'{equalPrefix}{str(package.newVersion)}'

            # run both changes in case the requirement is == or ~=
            updatedLine = regexSubstitute(pattern=equalPattern,  repl=repl, string=updatedLine)
            updatedLine = regexSubstitute(pattern=almostPattern, repl=repl, string=updatedLine)

        assert len(updatedLine) != 0, 'Developer error, bad regex'

        return updatedLine
