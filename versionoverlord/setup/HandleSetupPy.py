
from logging import Logger
from logging import getLogger

from os import environ as osEnvironment

from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE
from versionoverlord.exceptions.ProjectNotSetException import ProjectNotSetException
from versionoverlord.exceptions.ProjectsBaseNotSetException import ProjectsBaseNotSetException


STD_FILE_NAME: str = 'setup.py'


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

    def exists(self) -> bool:
        return True
