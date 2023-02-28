
from logging import Logger
from logging import getLogger

from os import sep as osSep

from pathlib import Path

from versionoverlord.Common import Packages
from versionoverlord.Common import REQUIREMENTS_TXT

from versionoverlord.exceptions.NoRequirementsTxtsException import NoRequirementsTxtException

from versionoverlord.BaseHandler import BaseHandler


class HandleRequirementsTxt(BaseHandler):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        super().__init__()

    def update(self, packages: Packages):

        requirementsTxtPath: Path = Path(f'{self._projectsBase}{osSep}{self._projectDirectory}{osSep}{REQUIREMENTS_TXT}')

        if requirementsTxtPath.exists() is False:
            raise NoRequirementsTxtException(fullPath=requirementsTxtPath)

