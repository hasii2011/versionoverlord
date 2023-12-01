
from typing import List

from logging import Logger
from logging import getLogger

from pathlib import Path

from os import linesep as osLineSep

from codeallybasic.SemanticVersion import SemanticVersion

from versionoverlord.Common import AdvancedSlugs
from versionoverlord.Common import REQUIREMENTS_TXT
from versionoverlord.Common import SPECIFICATION_FILE
from versionoverlord.Common import SlugVersion
from versionoverlord.Common import SlugVersions

from versionoverlord.EnvironmentBase import EnvironmentBase
from versionoverlord.GitHubAdapter import GitHubAdapter


class TemplateHandler(EnvironmentBase):

    def __init__(self, advancedSlugs: AdvancedSlugs):

        super().__init__()

        self.logger:         Logger        = getLogger(__name__)
        self._advancedSlugs: AdvancedSlugs = advancedSlugs

        requirementsPath:      Path      = Path(self._projectsBase) / self._projectDirectory / REQUIREMENTS_TXT
        self._requirementsTxt: List[str] = requirementsPath.read_text().split(osLineSep)

    def createSpecification(self):
        print(f'Creating a specification')
        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        slugVersions: SlugVersions = SlugVersions([])
        for advancedSlug in self._advancedSlugs:

            semanticVersion: SemanticVersion = gitHubAdapter.getLatestVersionNumber(advancedSlug.slug)
            slugVersion:     SlugVersion     = SlugVersion(slug=advancedSlug.slug, version=str(semanticVersion), packageName=advancedSlug.packageName)

            slugVersions.append(slugVersion)

        versionUpdateSpecification: Path = Path(SPECIFICATION_FILE)
        with versionUpdateSpecification.open(mode='w') as fd:
            fd.write(f'PackageName,OldVersion,NewVersion{osLineSep}')
            for slugVersion in slugVersions:

                oldVersion: str = self._findRequirementVersion(slugVersion.packageName)

                if oldVersion == '':
                    print(f'{slugVersion.slug} Did not find requirement')
                else:
                    fd.write(f'{slugVersion.packageName},{oldVersion},{slugVersion.version}{osLineSep}')

    def _findRequirementVersion(self, packageName: str) -> str:
        """
        Can handle requirements specifications like:
        pkgName==versionNumber
        pkgName~=versionNumber

        Args:
            packageName:   The package name to search for

        Returns:  A version number from the requirement file that matches the package name
                 If the requirement is not listed returns an empty string
        """
        lookupRequirement: str = f'{packageName}=='

        req: List[str] = self._searchRequirements(lookupRequirement)
        if len(req) == 0:
            lookupRequirement = f'{packageName}~='      # did not find '=='  how about '~='
            req = self._searchRequirements(lookupRequirement)
            if len(req) == 0:
                splitRequirement: List[str]  = ['', '']
            else:
                splitRequirement = req[0].split('~=')
        else:
            splitRequirement = req[0].split('==')

        return splitRequirement[1]

    def _searchRequirements(self, reqLine: str) -> List[str]:
        req = [match for match in self._requirementsTxt if reqLine in match]
        return req
