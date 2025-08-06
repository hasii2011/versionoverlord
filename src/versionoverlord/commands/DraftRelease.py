
from typing import cast

from requests.exceptions import ConnectionError

from click import command
from click import version_option
from click import option
from click import ClickException

from semantic_version import Version as SemanticVersion

from versionoverlord import __version__

from versionoverlord.Common import EPILOG
from versionoverlord.Common import RepositorySlug
from versionoverlord.Common import setUpLogging
from versionoverlord.Common import NO_INTERNET_CONNECTION_MSG

from versionoverlord.githubadapter.GitHubAdapter import GitHubAdapter
from versionoverlord.githubadapter.GitHubAdapterTypes import AdapterMilestone
from versionoverlord.githubadapter.GitHubAdapterError import GitHubAdapterError

from versionoverlord.commands.TagType import TagType

RELEASE_STUB_MESSAGE_TEMPLATE: str = 'See issues associated with this [milestone]({})'


@command(epilog=EPILOG)
@version_option(version=f'{__version__}', message='%(prog)s version %(version)s')
@option('--slug',      '-s', required=True,                 help='GitHub slug')
@option('--tag',       '-t', required=True, type=TagType(), help='Tag for release as a semantic version')
@option('--milestone', '-m', is_flag=True,                  help='Create associated milestone')
def draftRelease(slug: RepositorySlug, tag: TagType, milestone: bool):
    """
    \b
    This command creates draft release in the appropriate repository.
    You must provide a repository slug.
    The tag is a string that complies with the Semantic Version specification
    Specify the milestone if you want to created an associated milestone

    It uses the following environment variables:

    \b
        GH_TOKEN      – A personal GitHub access token necessary to read repository release information
        PROJECTS_BASE – The local directory where the python projects are based
        PROJECT       – The name of the project;  It should be a directory name
    """
    try:
        gitHubAdapter: GitHubAdapter = GitHubAdapter()
        milestoneUrl: str = ''

        # noinspection PySimplifyBooleanCheck
        if milestone is True:
            milestoneTitle: str = f'Release {tag}'
            adapterMilestone: AdapterMilestone = gitHubAdapter.createMilestone(repositorySlug=slug, title=milestoneTitle)
            milestoneUrl = adapterMilestone.milestoneUrl

        message: str = RELEASE_STUB_MESSAGE_TEMPLATE.format(milestoneUrl)
        gitHubAdapter.createDraftRelease(repositorySlug=slug, tag=cast(SemanticVersion, tag), message=message)
    except GitHubAdapterError as e:
        raise ClickException(message=e.message)
    except ConnectionError:
        raise ClickException(NO_INTERNET_CONNECTION_MSG)


if __name__ == "__main__":
    setUpLogging()
    # noinspection SpellCheckingInspection
    # createSpecification(['-i', 'tests/resources/testdata/query.slg'])
    # createSpecification(['-s', 'hasii2011/code-ally-basic,codeallybasic'])
    # -s hasii2011/ -s hasii2011/buildlackey

    # draftRelease(['--version'])
    # draftRelease(['--help'])
    draftRelease(['--slug', 'hasii2011/TestRepository1', '--tag', '10.0.0'])
