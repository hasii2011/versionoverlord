from pathlib import Path


class NoSetupPyFileException(Exception):

    def __init__(self, fullProjectPath: Path):

        self._fullProjectPath: Path = fullProjectPath

    @property
    def _ullProjectPath(self) -> Path:
        return self._fullProjectPath
