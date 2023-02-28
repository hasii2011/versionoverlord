from typing import Callable
from typing import List
from typing import NewType

from dataclasses import dataclass
from dataclasses import field

from versionoverlord.SemanticVersion import SemanticVersion


ENV_PROJECTS_BASE:    str = 'PROJECTS_BASE'
ENV_PROJECT:          str = 'PROJECT'
ENV_APPLICATION_NAME: str = 'APPLICATION_NAME'


SETUP_PY:         str = 'setup.py'
REQUIREMENTS_TXT: str = 'requirements.txt'


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


Packages = NewType('Packages', List[UpdatePackage])

# ActiveProjectInformationCallback  = Callable[[ActiveProjectInformation], None]
UpdateDependencyCallback = NewType('UpdateDependencyCallback', Callable[[str, Packages], str])    # type: ignore
