
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import Tuple

from dataclasses import dataclass
from dataclasses import field

from hasiicommon.SemanticVersion import SemanticVersion

ENV_PROJECTS_BASE:    str = 'PROJECTS_BASE'
ENV_PROJECT:          str = 'PROJECT'
ENV_APPLICATION_NAME: str = 'APPLICATION_NAME'


SETUP_PY:         str = 'setup.py'
REQUIREMENTS_TXT: str = 'requirements.txt'
INSTALL_REQUIRES: str = 'install_requires'

CIRCLE_CI_DIRECTORY: str = '.circleci'
CIRCLE_CI_YAML:      str = 'config.yml'

TEMPLATE_FILE:                str = 'versionUpdate.csv'


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

PackageLookupType = NewType('PackageLookupType', Dict[PackageName, UpdatePackage])

UpdateDependencyCallback = NewType('UpdateDependencyCallback', Callable[[str], str])    # type: ignore

Slugs = NewType('Slugs', Tuple[str])
