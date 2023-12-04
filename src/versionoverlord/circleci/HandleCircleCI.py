
from logging import Logger
from logging import getLogger

from os import sep as osSep

from pathlib import Path

from versionoverlord.Common import CIRCLE_CI_DIRECTORY
from versionoverlord.Common import CIRCLE_CI_YAML

from versionoverlord.IHandler import IHandler
from versionoverlord.Common import Packages

PIP_COMMAND: str = 'pip install'


class HandleCircleCI(IHandler):

    def __init__(self, packages: Packages):

        self.logger: Logger = getLogger(__name__)

        super().__init__(packages)

        self._circleCIYAML: Path = Path(f'{self._projectsBase}{osSep}{self._projectDirectory}{osSep}{CIRCLE_CI_DIRECTORY}{osSep}{CIRCLE_CI_YAML}')

    @property
    def configurationExists(self) -> bool:
        return self._circleCIYAML.exists()

    def update(self):

        circleCIYAML: Path = self._circleCIYAML

        with open(circleCIYAML, 'rt') as inputFd:
            content: str = inputFd.read()

        assert inputFd.closed, 'Should be auto closed'
        self.logger.info(f'{content=}')

        updatedContent: str = self._updateDependencies(content)
        self.logger.info(f'{updatedContent=}')

        with open(circleCIYAML, 'wt') as outputFd:
            outputFd.write(updatedContent)

        assert inputFd.closed, 'Should be auto closed'
