
from pathlib import Path

from click import command
from click import option
from click import secho

from click import version_option

from versionoverlord import __version__

from versionoverlord.Common import AdvancedSlugs
from versionoverlord.Common import CLISlugs
from versionoverlord.Common import extractCLISlugs
from versionoverlord.Common import setUpLogging

from versionoverlord.FileNameToSlugs import FileNameToSlugs
from versionoverlord.SlugHandler import SlugHandler


@command()
@version_option(version=f'{__version__}')
@option('--slugs',      '-s', required=False, multiple=True, help='GitHub slugs to query')
@option('--input-file', '-i', required=False,                help='Use input file for slug list')
def querySlugs(slugs: CLISlugs, input_file):
    """
        \b
        This command reads the repository for each input slug and displays
        their latest release version

        Input slugs can be on the command line or via file input
        \b
        It uses the following environment variables:

        \b
        GITHUB_ACCESS_TOKEN - A personal GitHub access token necessary to read repository
                              release information
    """
    if input_file is None:
        advancedSlugs: AdvancedSlugs = extractCLISlugs(slugs=slugs)
        slugHandler:   SlugHandler   = SlugHandler(advancedSlugs=advancedSlugs)

        slugHandler.handleSlugs()
    else:
        fqFileName: Path = Path(input_file)
        if fqFileName.exists() is False:
            secho('                          ', fg='red', bg='black', bold=True)
            secho('Input file does not exist ', fg='red', bg='black', bold=True)
            secho('                          ', fg='red', bg='black', bold=True)
        else:
            fileNameToSlugs: FileNameToSlugs = FileNameToSlugs(path=fqFileName)
            inputSlugs:      AdvancedSlugs   = fileNameToSlugs.getSlugs()
            handler:         SlugHandler     = SlugHandler(advancedSlugs=inputSlugs)
            handler.handleSlugs()


if __name__ == "__main__":
    setUpLogging()
    querySlugs()
