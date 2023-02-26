from dataclasses import field
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from pathlib import Path

from re import sub as regexSubstitute

from os import environ as osEnvironment
from os import sep as osSep

from tempfile import gettempdir
from tempfile import mkstemp

from versionoverlord.SemanticVersion import SemanticVersion

from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE
from versionoverlord.Common import SETUP_PY

from versionoverlord.exceptions.NoSetupPyFileException import NoSetupPyFileException
from versionoverlord.exceptions.ProjectNotSetException import ProjectNotSetException
from versionoverlord.exceptions.ProjectsBaseNotSetException import ProjectsBaseNotSetException


def versionFactory() -> SemanticVersion:
    return SemanticVersion('0.0.0')


PackageName = NewType('PackageName',    str)


@dataclass
class UpdatePackage:
    """
    Defines the package to update
    """
    packageName: PackageName     = PackageName('')
    oldVersion:  SemanticVersion = field(default_factory=versionFactory)
    newVersion:  SemanticVersion = field(default_factory=versionFactory)


Packages    = NewType('Packages', List[UpdatePackage])

STD_FILE_NAME: str = 'setup.py'
INSTALL_REQUIRES: str = 'install_requires'


class HandleSetupPy:
    """
    Handles the setup.py file
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        try:
            self._projectsBase: str = osEnvironment[ENV_PROJECTS_BASE]
        except KeyError:
            self.logger.error(f'Project Base not set')
            raise ProjectsBaseNotSetException
        try:
            self._projectDirectory: str = osEnvironment[ENV_PROJECT]
        except KeyError:
            self.logger.error(f'Project Directory not set')
            raise ProjectNotSetException

    def update(self, packages: Packages):
        """
        Updates a project's setup.py file.  Updates the "requires"
        Args:
            packages:    A list of UpdatePackage descriptions
        """
        setupPyPath: Path = Path(f'{self._projectsBase}{osSep}{self._projectDirectory}{osSep}{SETUP_PY}')

        if setupPyPath.exists() is False:
            raise NoSetupPyFileException(fullProjectPath=setupPyPath)

        self.logger.info(f'Working on: `{setupPyPath}`')

        osHandle, tempFile = mkstemp(text=True)
        with open(setupPyPath, 'r') as inputFd:
            with open(tempFile, 'w') as tempFileFd:
                self.logger.debug(f'tempDir: {gettempdir()}')
                while True:
                    contentLine: str = inputFd.readline()
                    if not contentLine:
                        break
                    # Check to see if we need to modify this line
                    # looking for a line like this:  install_requires=['ogl==0.70.20', 'untangle==1.2.1']
                    if INSTALL_REQUIRES in contentLine:
                        contentLine = self._updateRequires(contentLine, packages=packages)
                        self.logger.info(f'{contentLine=}')
                    tempFileFd.write(contentLine)

        # Replace with updated contents
        tempFilePath: Path = Path(tempFile)
        tempFilePath.rename(setupPyPath)

        self.logger.info(f'Break to here')

    def _updateRequires(self, contentLine: str, packages: Packages) -> str:
        """
        Updates the "requires" string
        Handles "==" and "~=" types

        Args:
            contentLine: The line to update
            packages:    A list of UpdatePackage descriptions

        Returns:  The updated string
        """
        updatedLine: str = contentLine
        for pkg in packages:
            package: UpdatePackage = cast(UpdatePackage, pkg)

            equalPrefix:  str = f'{package.packageName}=='
            almostPrefix: str = f'{package.packageName}~='

            equalPattern:  str = f'{equalPrefix}{package.oldVersion.__str__()}'
            almostPattern: str = f'{almostPrefix}{package.oldVersion.__str__()}'
            repl:          str = f'{equalPrefix}{package.newVersion.__str__()}'

            # run both changes in case the requirement is == or ~=
            updatedLine = regexSubstitute(pattern=equalPattern,  repl=repl, string=updatedLine)
            updatedLine = regexSubstitute(pattern=almostPattern, repl=repl, string=updatedLine)

        assert len(updatedLine) != 0, 'Developer error, bad regex'

        return updatedLine

    def exists(self) -> bool:
        return True
