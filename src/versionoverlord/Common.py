
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import Tuple

import logging
import logging.config

from importlib.abc import Traversable

from importlib.resources import files

from json import load as jsonLoad

from dataclasses import dataclass
from dataclasses import field

from codeallybasic.SemanticVersion import SemanticVersion


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
JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"


def versionFactory() -> SemanticVersion:
    return SemanticVersion('0.0.0')


PackageName = NewType('PackageName', str)


@dataclass
class UpdatePackage:
    """
    Defines the package to update
    """
    packageName: PackageName     = PackageName('')
    oldVersion:  SemanticVersion = field(default_factory=versionFactory)
    newVersion:  SemanticVersion = field(default_factory=versionFactory)


Packages                 = NewType('Packages', List[UpdatePackage])
PackageLookupType        = NewType('PackageLookupType', Dict[PackageName, UpdatePackage])
UpdateDependencyCallback = NewType('UpdateDependencyCallback', Callable[[str], str])    # type: ignore
CLISlugs                 = NewType('CLISlugs', Tuple[str])


@dataclass
class AdvancedSlug:
    slug:        str = ''
    packageName: str = ''


AdvancedSlugs = NewType('AdvancedSlugs', List[AdvancedSlug])


@dataclass
class SlugVersion(AdvancedSlug):
    version:     str = ''


SlugVersions = NewType('SlugVersions', List[SlugVersion])


def setUpLogging():
    """
    """
    traversable: Traversable = files(RESOURCES_PACKAGE_NAME) / JSON_LOGGING_CONFIG_FILENAME

    # loggingConfigFilename: str = resource_filename(RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)
    loggingConfigFilename: str = str(traversable)

    with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
        configurationDictionary = jsonLoad(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False


def extractPackageName(slug: str) -> str:
    splitSlug: List[str] = slug.split(sep='/')

    pkgName: str = splitSlug[1]
    return pkgName


def extractCLISlugs(slugs: CLISlugs) -> AdvancedSlugs:

    cliSlugs: AdvancedSlugs = AdvancedSlugs([])

    for slug in slugs:

        advancedSlug: AdvancedSlug = AdvancedSlug()
        slugPackage: List[str] = slug.split(',')
        if len(slugPackage) > 1:
            advancedSlug.slug = slugPackage[0]
            advancedSlug.packageName = slugPackage[1]
        else:
            advancedSlug.slug = slug
            advancedSlug.packageName = extractPackageName(slug)

        cliSlugs.append(advancedSlug)

    return cliSlugs
