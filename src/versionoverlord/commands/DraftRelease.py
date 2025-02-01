
from typing import cast

from click import command
from click import version_option
from click import option
from click import secho

from semantic_version import Version as SemanticVersion

from versionoverlord import __version__
from versionoverlord.Common import EPILOG
from versionoverlord.Common import RepositorySlug

from versionoverlord.Common import setUpLogging
from versionoverlord.githubadapter.GitHubAdapter import GitHubAdapter
from versionoverlord.commands.TagType import TagType


@command(epilog=EPILOG)
@version_option(version=f'{__version__}', message='%(prog)s version %(version)s')
@option('--slug',      '-s', required=True,                 help='GitHub slug')
@option('--tag',       '-t', required=True, type=TagType(), help='Tag for release as a semantic version')
def draftRelease(slug: RepositorySlug, tag: TagType):
    """
    \b
    This command creates draft release in the appropriate repository.
    You must provide a repository slug.
    The tag is a string that complies with the Semantic Version specification

    It uses the following environment variables:

    \b
        GH_TOKEN      – A personal GitHub access token necessary to read repository release information
        PROJECTS_BASE – The local directory where the python projects are based
        PROJECT       – The name of the project;  It should be a directory name
    """
    secho(f'{slug=} {tag}')

    gitHubAdapter: GitHubAdapter = GitHubAdapter()

    gitHubAdapter.createDraftRelease(repositorySlug=slug, tag=cast(SemanticVersion, tag))


if __name__ == "__main__":
    setUpLogging()
    # noinspection SpellCheckingInspection
    # createSpecification(['-i', 'tests/resources/testdata/query.slg'])
    # createSpecification(['-s', 'hasii2011/code-ally-basic,codeallybasic'])
    # -s hasii2011/ -s hasii2011/buildlackey

    # draftRelease(['--version'])
    # draftRelease(['--help'])
    draftRelease(['--slug', 'hasii2011/TestRepository', '--tag', '10.0.0'])
