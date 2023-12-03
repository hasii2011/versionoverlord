
from typing import Dict
from typing import cast

from logging import Logger
from logging import getLogger

import csv

from pathlib import Path as PyPath

from click import Path
from click import argument
from click import clear
from click import command
from click import echo
from click import option
from click import secho
from click import version_option

from codeallybasic.SemanticVersion import SemanticVersion

from versionoverlord import __version__

from versionoverlord.Common import PackageName
from versionoverlord.Common import Packages
from versionoverlord.Common import UpdatePackage
from versionoverlord.Common import setUpLogging

from versionoverlord.setup.HandleSetupPy import HandleSetupPy

from versionoverlord.circleci.HandleCircleCI import HandleCircleCI

from versionoverlord.pyprojecttoml.HandlePyProjectToml import HandlePyProjectToml

from versionoverlord.requirements.HandleRequirementsTxt import HandleRequirementsTxt


class UpdateDependencies:
    def __init__(self, specification: PyPath):
        self.logger: Logger = getLogger(__name__)

        self._packages: Packages = self._buildPackagesToUpdate(specification=specification)

    def update(self):

        assert len(self._packages) != 0,  'Developer error; package list not initialized'
        hsp: HandleSetupPy = HandleSetupPy(packages=self._packages)
        if hsp.configurationExists is True:
            echo('Update setup.py', color=True)
            hsp.update()
        else:
            echo('No setup.py')

        handleCircleCI: HandleCircleCI = HandleCircleCI(packages=self._packages)
        if handleCircleCI.configurationExists is True:
            echo('Update config.yml', color=True)
            handleCircleCI.update()
        else:
            echo("No config.yml")

        hrt: HandleRequirementsTxt = HandleRequirementsTxt(packages=self._packages)
        if hrt.configurationExists is True:
            echo('Update requirements.txt', color=True)
            hrt.update()
        else:
            echo('No requirements.txt')

        tomlHandler: HandlePyProjectToml = HandlePyProjectToml(packages=self._packages)
        if tomlHandler.configurationExists is True:
            echo('Update pyproject.toml', color=True)
            tomlHandler.update()
        else:
            echo('No pyproject.toml')

    def _buildPackagesToUpdate(self, specification: PyPath) -> Packages:
        with open(specification) as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            packages: Packages = Packages([])

            for dictRow in csvreader:
                row: Dict[str, str] = cast(Dict[str, str], dictRow)
                self.logger.debug(row['PackageName'], row['OldVersion'], row['NewVersion'])
                packageName: PackageName = PackageName(row['PackageName'])
                updatePackage: UpdatePackage = UpdatePackage()
                updatePackage.packageName = packageName
                updatePackage.oldVersion = SemanticVersion(row['OldVersion'])
                updatePackage.newVersion = SemanticVersion(row['NewVersion'])
                packages.append(updatePackage)

        return packages


@command()
@version_option(version=f'{__version__}', message='%(prog)s version %(version)s')
@option('--specification', '-s', is_flag=False, flag_value='versionSpecification.csv', default='versionSpecification.csv',
        type=Path(exists=True, path_type=PyPath),
        required=False,
        help='Update the project using a specification file')
@argument('projectsBase', envvar='PROJECTS_BASE')
@argument('project', envvar='PROJECT')
def updateDependencies(projectsbase: str, project: str, specification: PyPath):
    """
    \b
    This command uses the .csv file created by createSpec

    It uses the following environment variables:

    \b
        GITHUB_ACCESS_TOKEN - A personal GitHub access token necessary to read repository release information
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    """
    clear()
    secho(f'The project`s base directory {projectsbase}', color=True, reverse=True)
    secho(f'Project to update: {project}', color=True, reverse=True)
    secho('')
    setUpLogging()
    vUpdate: UpdateDependencies = UpdateDependencies(specification=specification)
    vUpdate.update()


if __name__ == "__main__":
    updateDependencies()
