
from logging import Logger
from logging import getLogger

from click import ClickException
from click import secho

from semantic_version import Version as SemanticVersion

from versionoverlord.Common import AdvancedSlugs
from versionoverlord.Common import ENV_GH_TOKEN
from versionoverlord.Common import SlugVersion
from versionoverlord.Common import SlugVersions

from versionoverlord.DisplayVersions import DisplayVersions

from versionoverlord.GitHubAdapter import GitHubAdapter

from versionoverlord.githubadapter.exceptions.NoGitHubAccessTokenException import NoGitHubAccessTokenException
from versionoverlord.githubadapter.exceptions.UnknownGitHubRepositoryException import UnknownGitHubRepositoryException


class SlugHandler:
    def __init__(self, advancedSlugs: AdvancedSlugs):

        self.logger:         Logger        = getLogger(__name__)
        self._advancedSlugs: AdvancedSlugs = advancedSlugs

    def handleSlugs(self):
        try:
            gitHubAdapter: GitHubAdapter = GitHubAdapter()

            slugVersions: SlugVersions = SlugVersions([])
            for advancedSlug in self._advancedSlugs:

                version:     SemanticVersion = gitHubAdapter.getLatestVersionNumber(advancedSlug.slug)
                slugVersion: SlugVersion     = SlugVersion(slug=advancedSlug.slug, version=str(version))
                slugVersions.append(slugVersion)

            if len(slugVersions) == 0:
                secho('Nothing to see here')
            else:
                displayVersions: DisplayVersions = DisplayVersions()
                displayVersions.displaySlugs(slugVersions=slugVersions)
        except NoGitHubAccessTokenException:
            raise ClickException(f'Your must provide a GitHub access token via the environment variable `{ENV_GH_TOKEN}`')
        except UnknownGitHubRepositoryException as e:
            raise ClickException(f'Unknown GitHub Repository: `{e.repositorySlug}`')
        except (ValueError, Exception) as e:
            print(f'{e}')
