from typing import List
from typing import Tuple

import logging.config

from json import load as jsonLoad

from pathlib import Path

from os import linesep as osLineSep
from typing import cast

from click import command
from click import option
from click import version_option

from pkg_resources import resource_filename

from versionoverlord.DisplayVersions import SlugVersion
from versionoverlord.DisplayVersions import SlugVersions
from versionoverlord.GitHubAdapter import GitHubAdapter
from versionoverlord.SlugHandler import SlugHandler
from versionoverlord.SlugHandler import Slugs
from versionoverlord.SemanticVersion import SemanticVersion


__version__ = "0.2.0"

RESOURCES_PACKAGE_NAME:       str = 'versionoverlord.resources'
JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfig.json"
TEMPLATE_FILE:                str = 'versionUpdate.csv'


def setUpLogging():
    """"""

    loggingConfigFilename: str = resource_filename(RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

    with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
        configurationDictionary = jsonLoad(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False


def handleCreateTemplate(slugs: Tuple[str]):
    print(f'Creating a template')
    versionOverlord: GitHubAdapter = GitHubAdapter()

    slugVersions: SlugVersions = SlugVersions([])
    for slug in slugs:
        version: SemanticVersion = versionOverlord.getLatestVersionNumber(slug)
        slugVersion: SlugVersion = SlugVersion(slug=slug, version=version.__str__())
        slugVersions.append(slugVersion)

    versionUpdateTemplate: Path = Path(TEMPLATE_FILE)
    with versionUpdateTemplate.open(mode='w') as fd:
        for slugVersion in slugVersions:
            pkgName: str = extractPackageName(slug=slugVersion.slug)
            print(f'{pkgName},{slugVersion.version},NewVersionGoesHere')
            fd.write(f'{pkgName},{slugVersion.version},NewVersionGoesHere{osLineSep}')


def extractPackageName(slug: str) -> str:
    splitSlug: List[str] = slug.split(sep='/')

    pkgName: str = splitSlug[1]
    return pkgName


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('--slugs', '-s',  multiple=True, required=False, help='GitHub slugs to query')
@option('--create', '-c', multiple=True, required=False, help='Create template package versions')
def commandHandler(slugs: Tuple[str], create: Tuple[str]):

    if len(slugs) != 0:
        slugHandler: SlugHandler = SlugHandler(slugs=cast(Slugs, slugs))
        slugHandler.handleSlugs()
    if len(create) != 0:
        handleCreateTemplate(create)


if __name__ == "__main__":
    setUpLogging()
    commandHandler()
