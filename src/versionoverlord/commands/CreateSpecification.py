
from pathlib import Path
from typing import List
from typing import Tuple

from click import command
from click import option
from click import secho
from click import version_option

from versionoverlord import __version__
from versionoverlord.Common import AdvancedSlug
from versionoverlord.Common import AdvancedSlugs

from versionoverlord.Common import extractPackageName
from versionoverlord.Common import setUpLogging

from versionoverlord.FileNameToSlugs import FileNameToSlugs
from versionoverlord.TemplateHandler import TemplateHandler


# noinspection SpellCheckingInspection
@command()
@version_option(version=f'{__version__}', message='%(prog)s version %(version)s')
@option('--slugs',     '-s',  multiple=True, required=False, help='Create package update specification')
@option('--input-file', '-i', required=False,                help='Use input file for slug list')
def createSpecification(slugs: Tuple[str], input_file: str):
    """
    \b
    This command creates .csv specification file
    It uses the following environment variables:
    \b
        GITHUB_ACCESS_TOKEN - A personal GitHub access token necessary to read repository release information
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    """

    if len(slugs) != 0:
        cliSlugs: AdvancedSlugs = AdvancedSlugs([])
        for slug in slugs:
            advancedSlug: AdvancedSlug = AdvancedSlug()
            slugPackage:  List[str] = slug.split(',')
            if len(slugPackage) > 1:
                advancedSlug.slug        = slugPackage[0]
                advancedSlug.packageName = slugPackage[1]
            else:
                advancedSlug.slug        = slug
                advancedSlug.packageName = extractPackageName(slug)
            cliSlugs.append(advancedSlug)

        templateHandler: TemplateHandler = TemplateHandler(cliSlugs)
        templateHandler.createSpecification()
    elif input_file is not None:
        fqFileName: Path = Path(input_file)
        if fqFileName.exists() is False:
            secho('                          ', fg='red', bg='black', bold=True)
            secho('Input file does not exist ', fg='red', bg='black', bold=True)
            secho('                          ', fg='red', bg='black', bold=True)
        else:
            fileNameToSlugs: FileNameToSlugs = FileNameToSlugs(path=fqFileName)
            fileSlugs:           AdvancedSlugs   = fileNameToSlugs.getSlugs()

            templateHandler = TemplateHandler(advancedSlugs=fileSlugs)
            templateHandler.createSpecification()


if __name__ == "__main__":
    setUpLogging()
    # noinspection SpellCheckingInspection
    createSpecification(['-i', 'tests/resources/testdata/query.slg'])
    # createSpecification(['-s', 'hasii2011/code-ally-basic,codeallybasic'])
    # createSpecification(['-s', 'hasii2011/buildlackey'])
