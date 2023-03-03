
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from abc import ABC
from abc import abstractmethod

from os import environ as osEnvironment

from pathlib import Path

from tempfile import gettempdir

from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE
from versionoverlord.Common import PackageLookupType
from versionoverlord.Common import Packages
from versionoverlord.Common import UpdateDependencyCallback
from versionoverlord.Common import UpdatePackage

from versionoverlord.exceptions.ProjectNotSetException import ProjectNotSetException
from versionoverlord.exceptions.ProjectsBaseNotSetException import ProjectsBaseNotSetException


class BaseHandler(ABC):
    def __init__(self, packages: Packages):

        self._packages:  Packages = packages
        self.baseLogger: Logger   = getLogger(__name__)

        try:
            self._projectsBase: str = osEnvironment[ENV_PROJECTS_BASE]
        except KeyError:
            self.baseLogger.error(f'Project Base not set')
            raise ProjectsBaseNotSetException
        try:
            self._projectDirectory: str = osEnvironment[ENV_PROJECT]
        except KeyError:
            self.baseLogger.error(f'Project Directory not set')
            raise ProjectNotSetException
        except (ValueError, Exception) as e:
            self.baseLogger.error(f'{e}')

        self._packageDict: PackageLookupType = self._buildPackageLookup()

    @abstractmethod
    def update(self):
        """
        Updates a project's file.
        """
        pass

    def _fixDependencies(self, searchFile: Path, tempFile: str, searchItems: List[str], callback: UpdateDependencyCallback):
        """

        Args:
            searchFile:     The file we will iterate through
            tempFile:       The temporary file to write the changed file
            searchItems:    A list of strings to find
            callback:       The method to call when we find a match;
        """
        self.baseLogger.info(f'{searchItems=}')
        self.baseLogger.info(f'{tempFile=}')
        with open(searchFile, 'r') as inputFd:
            with open(tempFile, 'w') as tempFileFd:
                self.baseLogger.debug(f'tempDir: {gettempdir()}')
                while True:
                    contentLine: str = inputFd.readline()
                    if not contentLine:
                        break

                    # Check to see if we need to modify this line
                    for searchText in searchItems:
                        if searchText in contentLine:
                            contentLine = callback(contentLine)
                            self.baseLogger.info(f'{contentLine=}')
                    tempFileFd.write(contentLine)

    def _buildPackageLookup(self) -> PackageLookupType:

        lookupDict: PackageLookupType = PackageLookupType({})

        for pkg in self._packages:
            updatePackage: UpdatePackage = cast(UpdatePackage, pkg)
            lookupDict[updatePackage.packageName] = updatePackage

        return lookupDict
