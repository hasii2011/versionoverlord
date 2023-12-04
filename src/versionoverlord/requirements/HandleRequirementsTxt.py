
from logging import Logger
from logging import getLogger

from os import sep as osSep

from pathlib import Path

from versionoverlord.Common import REQUIREMENTS_TXT
from versionoverlord.Common import Packages

from versionoverlord.IHandler import IHandler


class HandleRequirementsTxt(IHandler):

    def __init__(self, packages: Packages):

        self.logger: Logger = getLogger(__name__)

        super().__init__(packages)

        self._requirementsTxtPath: Path = Path(f'{self._projectsBase}{osSep}{self._projectDirectory}{osSep}{REQUIREMENTS_TXT}')

    @property
    def configurationExists(self) -> bool:
        return self._requirementsTxtPath.exists()

    def update(self):

        requirementsTxtPath: Path = self._requirementsTxtPath

        with open(requirementsTxtPath, 'rt') as inputFd:
            content: str = inputFd.read()

        assert inputFd.closed, 'Should be auto closed'
        self.logger.info(f'{content=}')

        updatedContent: str = self._updateDependencies(content)
        self.logger.info(f'{updatedContent=}')

        with open(requirementsTxtPath, 'wt') as outputFd:
            outputFd.write(updatedContent)

        assert inputFd.closed, 'Should be auto closed'
