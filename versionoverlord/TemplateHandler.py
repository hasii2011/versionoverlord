
from typing import List

from logging import Logger
from logging import getLogger

from pathlib import Path

from os import linesep as osLineSep

from versionoverlord.Common import Slugs
from versionoverlord.Common import TEMPLATE_FILE
from versionoverlord.DisplayVersions import SlugVersion
from versionoverlord.DisplayVersions import SlugVersions
from versionoverlord.GitHubAdapter import GitHubAdapter
from versionoverlord.SemanticVersion import SemanticVersion


class TemplateHandler:
    def __init__(self, slugs: Slugs):

        self.logger: Logger = getLogger(__name__)
        self._slugs: Slugs  = slugs

    def createTemplate(self):
        print(f'Creating a template')
        versionOverlord: GitHubAdapter = GitHubAdapter()

        slugVersions: SlugVersions = SlugVersions([])
        for slug in self._slugs:
            version: SemanticVersion = versionOverlord.getLatestVersionNumber(slug)
            slugVersion: SlugVersion = SlugVersion(slug=slug, version=str(version))
            slugVersions.append(slugVersion)

        versionUpdateTemplate: Path = Path(TEMPLATE_FILE)
        with versionUpdateTemplate.open(mode='w') as fd:
            for slugVersion in slugVersions:
                pkgName: str = self._extractPackageName(slug=slugVersion.slug)
                print(f'{pkgName},{slugVersion.version},NewVersionGoesHere')
                fd.write(f'{pkgName},{slugVersion.version},NewVersionGoesHere{osLineSep}')

    def _extractPackageName(self, slug: str) -> str:
        splitSlug: List[str] = slug.split(sep='/')

        pkgName: str = splitSlug[1]
        return pkgName
