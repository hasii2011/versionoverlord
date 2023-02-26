
from typing import cast

from logging import Logger
from logging import getLogger
import logging.config

from json import load as jsonLoad

from collections import Counter

from os import environ as osEnvironment

from click import command
from click import option
from click import version_option
from github import Github
from github import UnknownObjectException

from github.GitRelease import GitRelease
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from pkg_resources import resource_filename

from versionoverlord.DisplayVersions import DisplayVersions
from versionoverlord.DisplayVersions import SlugVersion
from versionoverlord.DisplayVersions import SlugVersions
from versionoverlord.exceptions.NoGitHubAccessTokenException import NoGitHubAccessTokenException
from versionoverlord.SemanticVersion import SemanticVersion


__version__ = "0.1.0"

from versionoverlord.exceptions.UnknownGitHubRepositoryException import UnknownGitHubRepositoryException


RESOURCES_PACKAGE_NAME: str = 'versionoverlord.resources'
JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfig.json"


def setUpLogging():
    """"""

    loggingConfigFilename: str = resource_filename(RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

    with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
        configurationDictionary = jsonLoad(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False


class VersionOverlord:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        try:
            gitHubToken: str = osEnvironment['GITHUB_ACCESS_TOKEN']
        except KeyError:
            raise NoGitHubAccessTokenException

        self._github: Github = Github(gitHubToken)

    def getLatestVersionNumber(self, repositorySlug: str) -> SemanticVersion:

        try:
            repo: Repository = self._github.get_repo(repositorySlug)
            self.logger.debug(f'{repo.full_name=}')
        except UnknownObjectException:
            raise UnknownGitHubRepositoryException(repositorySlug=repositorySlug)

        releases: PaginatedList = repo.get_releases()

        latestReleaseVersion: SemanticVersion = SemanticVersion('0.0.0')
        for release in releases:
            gitRelease: GitRelease = cast(GitRelease, release)

            releaseNumber: str = gitRelease.tag_name
            numPeriods: int = self._countPeriods(releaseNumber)
            if numPeriods < 2:
                releaseNumber = f'{releaseNumber}.0'

            releaseVersion: SemanticVersion = SemanticVersion(releaseNumber)
            self.logger.debug(f'{releaseVersion=}')
            if latestReleaseVersion < releaseVersion:
                latestReleaseVersion = releaseVersion

        return latestReleaseVersion

    def _countPeriods(self, releaseNumber: str) -> int:

        cnt = Counter(list(releaseNumber))
        return cnt['.']


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('--slugs', '-s', multiple=True, help='GitHub slugs to query')
def commandHandler(slugs):

    try:
        versionOverlord: VersionOverlord = VersionOverlord()

        slugVersions: SlugVersions = SlugVersions([])
        for slug in slugs:
            version: SemanticVersion = versionOverlord.getLatestVersionNumber(slug)
            slugVersion: SlugVersion = SlugVersion(slug=slug, version=version.__str__())
            slugVersions.append(slugVersion)

        displayVersions: DisplayVersions = DisplayVersions()
        displayVersions.displaySlugs(slugVersions=slugVersions)
    except NoGitHubAccessTokenException:
        print(f'Your must provide a GitHub access token via the environment variable `GITHUB_ACCESS_TOKEN`')
    except UnknownGitHubRepositoryException as e:
        print(f'Unknown GitHub Repository: `{e.repositorySlug}`')
    except (ValueError, Exception) as e:
        print(f'{e}')


if __name__ == "__main__":
    setUpLogging()
    commandHandler()
