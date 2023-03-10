from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import Tuple

import logging
import logging.config

from json import load as jsonLoad

from dataclasses import dataclass
from dataclasses import field

from hasiicommon.SemanticVersion import SemanticVersion

from pkg_resources import resource_filename


__version__ = "0.3.0"


ENV_PROJECTS_BASE:    str = 'PROJECTS_BASE'
ENV_PROJECT:          str = 'PROJECT'
ENV_APPLICATION_NAME: str = 'APPLICATION_NAME'


SETUP_PY:         str = 'setup.py'
REQUIREMENTS_TXT: str = 'requirements.txt'
INSTALL_REQUIRES: str = 'install_requires'

CIRCLE_CI_DIRECTORY: str = '.circleci'
CIRCLE_CI_YAML:      str = 'config.yml'

SPECIFICATION_FILE:           str = 'versionSpecification.csv'
RESOURCES_PACKAGE_NAME:       str = 'versionoverlord.resources'
JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfig.json"


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


def setUpLogging():
    """"""

    loggingConfigFilename: str = resource_filename(RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

    with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
        configurationDictionary = jsonLoad(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False
