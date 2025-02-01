from typing import cast

from logging import Logger
from logging import getLogger

from collections import Counter

from os import environ as osEnvironment

from datetime import date
from datetime import timedelta

from github import Github
from github import UnknownObjectException
from github import GithubException

from github.GitRelease import GitRelease
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.Milestone import Milestone

from semantic_version import Version as SemanticVersion

from versionoverlord.Common import ENV_GH_TOKEN

from versionoverlord.Common import RepositorySlug
from versionoverlord.GitHubAdapterTypes import AdapterMilestone

from versionoverlord.GitHubAdapterTypes import AdapterRelease
from versionoverlord.GitHubAdapterTypes import ReleaseId
from versionoverlord.GitHubAdapterTypes import ReleaseName
from versionoverlord.GitHubAdapterTypes import ReleaseNumber

from versionoverlord.githubadapter.exceptions.GitHubAdapterError import GitHubAdapterError
from versionoverlord.githubadapter.exceptions.NoGitHubAccessTokenException import NoGitHubAccessTokenException
from versionoverlord.githubadapter.exceptions.UnknownGitHubRelease import UnknownGitHubRelease
from versionoverlord.githubadapter.exceptions.UnknownGitHubRepositoryException import UnknownGitHubRepositoryException

DEFAULT_RELEASE_STUB_MESSAGE:     str = 'See issues associated with this [milestone](url)'
DEFAULT_MILESTONE_DUE_DATE_DELTA: int = 7
DEFAULT_MILESTONE_STATE:          str = 'open'


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

    def createDraftRelease(self, repositorySlug: RepositorySlug, tag: SemanticVersion) -> AdapterRelease:
        """

        Args:
            repositorySlug:   A GitHub repository slug
            tag:              The tag number

        Returns:  The GitHub AdapterRelease Id

        """
        try:
            repo: Repository = self._github.get_repo(repositorySlug)
            self.logger.debug(f'{repo.full_name=}')
            releaseName: ReleaseName = ReleaseName(f'AdapterRelease {tag}')

            gitRelease: GitRelease = repo.create_git_release(tag=str(tag), name=releaseName, message=DEFAULT_RELEASE_STUB_MESSAGE, draft=True, prerelease=False, generate_release_notes=False)

        except UnknownObjectException:
            raise UnknownGitHubRepositoryException(repositorySlug=repositorySlug)

        release: AdapterRelease = AdapterRelease(
            id=ReleaseId(gitRelease.id),
            draft=gitRelease.draft,
            title=gitRelease.title,
            body=gitRelease.body,
            tag=SemanticVersion(gitRelease.tag_name)
        )
        return release

    def createMilestone(self, repositorySlug: RepositorySlug, title: str) -> AdapterMilestone:
        try:
            repo: Repository = self._github.get_repo(repositorySlug)
            self.logger.debug(f'{repo.full_name=}')

            today: date = date.today() + timedelta(days=DEFAULT_MILESTONE_DUE_DATE_DELTA)

            milestone: Milestone = repo.create_milestone(title=title,
                                                         state=DEFAULT_MILESTONE_STATE,
                                                         description='',
                                                         due_on=today)
            adapterMilestone: AdapterMilestone = AdapterMilestone(
                releaseNumber=ReleaseNumber(milestone.number),
                title=milestone.title,
                state=milestone.state,
                description=milestone.description,
                dueDate=milestone.due_on
            )
            return adapterMilestone

        except GithubException as ge:
            raise GitHubAdapterError(message=ge.__str__())

    def deleteMilestone(self, repositorySlug: RepositorySlug, releaseNumber: ReleaseNumber):
        """

        Args:
            repositorySlug: A GitHub repository slug
            releaseNumber:  An adapter ReleaseNumber
        """
        try:
            repo: Repository = self._github.get_repo(repositorySlug)
            self.logger.debug(f'{repo.full_name=}')

            milestone: Milestone = repo.get_milestone(number=releaseNumber)
            milestone.delete()

        except GithubException as ge:
            raise GitHubAdapterError(message=ge.__str__())

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
            # self.logger.error(f'{releaseId=} {e=}')
            raise UnknownGitHubRelease(message=f'AdapterRelease ID not found. {e=}')

    def _countPeriods(self, releaseNumber: str) -> int:

        cnt = Counter(list(releaseNumber))
        return cnt['.']
