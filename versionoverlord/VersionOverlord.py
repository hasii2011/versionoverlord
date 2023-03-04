
from typing import cast
from typing import Tuple

import logging.config

from json import load as jsonLoad

from click import command
from click import option
from click import version_option

from pkg_resources import resource_filename

from versionoverlord.SlugHandler import SlugHandler
from versionoverlord.SlugHandler import Slugs


__version__ = "0.2.0"

from versionoverlord.TemplateHandler import TemplateHandler


RESOURCES_PACKAGE_NAME:       str = 'versionoverlord.resources'
JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfig.json"


def setUpLogging():
    """"""

    loggingConfigFilename: str = resource_filename(RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

    with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
        configurationDictionary = jsonLoad(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('--slugs', '-s',  multiple=True, required=False, help='GitHub slugs to query')
@option('--create', '-c', multiple=True, required=False, help='Create template package versions')
def commandHandler(slugs: Tuple[str], create: Tuple[str]):

    if len(slugs) != 0:
        slugHandler: SlugHandler = SlugHandler(slugs=cast(Slugs, slugs))
        slugHandler.handleSlugs()
    if len(create) != 0:
        templateHandler: TemplateHandler = TemplateHandler(slugs=cast(Slugs, create))
        templateHandler.createTemplate()


if __name__ == "__main__":
    setUpLogging()
    commandHandler()
