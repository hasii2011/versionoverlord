
from typing import List

from logging import Logger
from logging import getLogger

from pathlib import Path

from os import linesep as osLineSep

from versionoverlord.Common import REQUIREMENTS_TXT
from versionoverlord.Common import TEMPLATE_FILE
from versionoverlord.Common import Slugs

from versionoverlord.DisplayVersions import SlugVersion
from versionoverlord.DisplayVersions import SlugVersions
from versionoverlord.EnvironmentBase import EnvironmentBase
from versionoverlord.GitHubAdapter import GitHubAdapter

from versionoverlord.SemanticVersion import SemanticVersion


class TemplateHandler(EnvironmentBase):

    def __init__(self, slugs: Slugs):

        super().__init__()

        self.logger: Logger = getLogger(__name__)
        self._slugs: Slugs  = slugs

        requirementsPath:      Path      = Path(self._projectsBase) / self._projectDirectory / REQUIREMENTS_TXT
        self._requirementsTxt: List[str] = requirementsPath.read_text().split(osLineSep)

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
            fd.write(f'PackageName,OldVersion,NewVersion{osLineSep}')
            for slugVersion in slugVersions:
                oldVersion: str = self._findRequirementVersion(self._extractPackageName(slugVersion.slug))
                pkgName: str = self._extractPackageName(slug=slugVersion.slug)
                fd.write(f'{pkgName},{oldVersion},{slugVersion.version}{osLineSep}')

    def _extractPackageName(self, slug: str) -> str:
        splitSlug: List[str] = slug.split(sep='/')

        pkgName: str = splitSlug[1]
        return pkgName

    def _findRequirementVersion(self, packageName: str) -> str:

        lookupRequirement: str = f'{packageName}=='

        req: List[str] = self._searchRequirements(lookupRequirement)
        if len(req) == 0:
            lookupRequirement = f'{packageName}~='
            req = self._searchRequirements(lookupRequirement)
            splitRequirement: List[str] = req[0].split('~=')
        else:
            splitRequirement = req[0].split('==')

        return splitRequirement[1]

    def _searchRequirements(self, reqLine: str) -> List[str]:
        req = [match for match in self._requirementsTxt if reqLine in match]
        return req
