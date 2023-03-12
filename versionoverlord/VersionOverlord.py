
from typing import cast
from typing import Tuple

from click import command
from click import option
from click import version_option

from versionoverlord.Common import setUpLogging
from versionoverlord.Common import __version__

from versionoverlord.SlugHandler import SlugHandler
from versionoverlord.SlugHandler import Slugs


from versionoverlord.TemplateHandler import TemplateHandler


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('--slugs', '-s',  multiple=True, required=False, help='GitHub slugs to query')
@option('--create', '-c', multiple=True, required=False, help='Create package update specification')
def commandHandler(slugs: Tuple[str], create: Tuple[str]):

    if len(slugs) != 0:
        slugHandler: SlugHandler = SlugHandler(slugs=cast(Slugs, slugs))
        slugHandler.handleSlugs()
    if len(create) != 0:
        templateHandler: TemplateHandler = TemplateHandler(slugs=cast(Slugs, create))
        templateHandler.createSpecification()


if __name__ == "__main__":
    setUpLogging()
    commandHandler()
