
from typing import cast

from logging import Logger
from logging import getLogger

from collections import Counter

from os import environ as osEnvironment

from github import Github
from github import UnknownObjectException
from github.GitRelease import GitRelease
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from semantic_version import Version as SemanticVersion

from versionoverlord.Common import ENV_GH_TOKEN
from versionoverlord.Common import ReleaseName
from versionoverlord.Common import RepositorySlug
from versionoverlord.exceptions.NoGitHubAccessTokenException import NoGitHubAccessTokenException
from versionoverlord.exceptions.UnknownGitHubRelease import UnknownGitHubRelease
from versionoverlord.exceptions.UnknownGitHubRepositoryException import UnknownGitHubRepositoryException

DEFAULT_RELEASE_STUB_MESSAGE: str = 'See issues associated with associated [milestone](url)'


class GitHubAdapter:
    """
    TODO:  As more methods get added I need to stop the leakage of GitHub objects

    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        try:
            gitHubToken: str = osEnvironment[ENV_GH_TOKEN]
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

            if gitRelease.draft is True:
                self.logger.warning(f'{repo.full_name} Ignore pre-release {gitRelease.tag_name}')
                continue
            releaseNumber: str = gitRelease.tag_name
            numPeriods: int = self._countPeriods(releaseNumber)
            if numPeriods < 2:
                releaseNumber = f'{releaseNumber}.0'

            releaseVersion: SemanticVersion = SemanticVersion.coerce(releaseNumber)
            self.logger.debug(f'{releaseVersion=}')
            if latestReleaseVersion < releaseVersion:
                latestReleaseVersion = releaseVersion

        return latestReleaseVersion

    def createDraftRelease(self, repositorySlug: RepositorySlug, tag: SemanticVersion) -> GitRelease:
        """
        TODO:  Maybe synthesize a git release object
        Args:
            repositorySlug:   A GitHub repository slug
            tag:              The tag number

        Returns:  The git release object (leakage here)

        """
        try:
            repo: Repository = self._github.get_repo(repositorySlug)
            self.logger.debug(f'{repo.full_name=}')
            releaseName: ReleaseName = ReleaseName(f'Release {tag}')

            gitRelease: GitRelease = repo.create_git_release(tag=str(tag), name=releaseName, message=DEFAULT_RELEASE_STUB_MESSAGE, draft=True, prerelease=False, generate_release_notes=False)

        except UnknownObjectException:
            raise UnknownGitHubRepositoryException(repositorySlug=repositorySlug)

        return gitRelease

    def deleteRelease(self, repositorySlug: RepositorySlug, releaseId: int):
        """

        Args:
            repositorySlug: A GitHub repository slug
            releaseId:      A git release ID

        """
        try:
            repo: Repository = self._github.get_repo(repositorySlug)
            self.logger.debug(f'{repo.full_name=}')

            gitRelease: GitRelease = repo.get_release(id=releaseId)
            gitRelease.delete_release()

        except UnknownObjectException as e:
            self.logger.error(f'{e=}')
            raise UnknownGitHubRelease(message='Release ID not found')

    def _countPeriods(self, releaseNumber: str) -> int:

        cnt = Counter(list(releaseNumber))
        return cnt['.']
