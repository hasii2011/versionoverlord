from typing import Callable
from typing import cast

from logging import Logger
from logging import getLogger

from pathlib import Path

from re import sub as regexSubstitute

from os import sep as osSep

from tempfile import gettempdir
from tempfile import mkstemp

from versionoverlord.Common import Packages
from versionoverlord.Common import UpdateDependencyCallback
from versionoverlord.Common import UpdatePackage
from versionoverlord.Common import SETUP_PY

from versionoverlord.exceptions.NoSetupPyFileException import NoSetupPyFileException

from versionoverlord.BaseHandler import BaseHandler

STD_FILE_NAME: str = 'setup.py'
INSTALL_REQUIRES: str = 'install_requires'


class HandleSetupPy(BaseHandler):
    """
    Handles the setup.py file
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)
        super().__init__()

    def update(self, packages: Packages):
        """
        Updates a project's setup.py file.  Updates the "requires"
        Args:
            packages:    A list of UpdatePackage descriptions
        """
        setupPyPath: Path = Path(f'{self._projectsBase}{osSep}{self._projectDirectory}{osSep}{SETUP_PY}')

        if setupPyPath.exists() is False:
            raise NoSetupPyFileException(fullPath=setupPyPath)

        self.logger.info(f'Working on: `{setupPyPath}`')

        osHandle, tempFile = mkstemp(text=True)
        self._fixDependencies(searchFile=setupPyPath, tempFile=tempFile, searchText=INSTALL_REQUIRES,
                              packages=packages,
                              callback=UpdateDependencyCallback(self._updateRequires))
        # with open(setupPyPath, 'r') as inputFd:
        #     with open(tempFile, 'w') as tempFileFd:
        #         self.logger.debug(f'tempDir: {gettempdir()}')
        #         while True:
        #             contentLine: str = inputFd.readline()
        #             if not contentLine:
        #                 break
        #             # Check to see if we need to modify this line
        #             # looking for a line like this:  install_requires=['ogl==0.70.20', 'untangle==1.2.1']
        #             if INSTALL_REQUIRES in contentLine:
        #                 contentLine = self._updateRequires(contentLine, packages=packages)
        #                 self.logger.info(f'{contentLine=}')
        #             tempFileFd.write(contentLine)

        # Replace with updated contents
        tempFilePath: Path = Path(tempFile)
        tempFilePath.rename(setupPyPath)

        self.logger.info(f'Break to here')

    def _fixDependencies(self, searchFile: Path, tempFile: str, searchText: str, packages: Packages, callback: UpdateDependencyCallback):
        self.logger.info(f'{searchText=}')

        with open(searchFile, 'r') as inputFd:
            with open(tempFile, 'w') as tempFileFd:
                self.logger.debug(f'tempDir: {gettempdir()}')
                while True:
                    contentLine: str = inputFd.readline()
                    if not contentLine:
                        break
                    # Check to see if we need to modify this line

                    if searchText in contentLine:
                        # contentLine = self._updateRequires(contentLine, packages=packages)
                        contentLine = callback(contentLine, packages)
                        self.logger.info(f'{contentLine=}')
                    tempFileFd.write(contentLine)

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
