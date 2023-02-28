from abc import ABC
from abc import abstractmethod
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment

from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE
from versionoverlord.Common import Packages

from versionoverlord.exceptions.ProjectNotSetException import ProjectNotSetException
from versionoverlord.exceptions.ProjectsBaseNotSetException import ProjectsBaseNotSetException


class BaseHandler(ABC):
    def __init__(self):

        self.baseLogger: Logger = getLogger(__name__)

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

    @abstractmethod
    def update(self, packages: Packages):
        """
        Updates a project's setup.py file.  Updates the "requires"
        Args:
            packages:    A list of UpdatePackage descriptions
        """
        pass
