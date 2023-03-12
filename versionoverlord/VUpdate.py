import csv
from logging import Logger
from logging import getLogger

from pathlib import Path as PyPath

from click import Path
from click import command
from click import echo
from click import option
from click import version_option
from hasiicommon.SemanticVersion import SemanticVersion

from versionoverlord.Common import PackageName
from versionoverlord.Common import Packages
from versionoverlord.Common import UpdatePackage
from versionoverlord.Common import __version__
from versionoverlord.Common import setUpLogging
from versionoverlord.circleci.HandleCircleCI import HandleCircleCI
from versionoverlord.requirements.HandleRequirementsTxt import HandleRequirementsTxt
from versionoverlord.setup.HandleSetupPy import HandleSetupPy


class VUpdate:
    def __init__(self, specification: PyPath):
        self.logger: Logger = getLogger(__name__)

        self._packages: Packages = self._buildPackagesToUpdate(specification=specification)

    def update(self):

        assert len(self._packages) != 0,  'Developer error; package list not initialized'
        echo('Update setup.py', color=True)
        hsp: HandleSetupPy = HandleSetupPy(packages=self._packages)
        hsp.update()

        echo('Update config.yml', color=True)
        handleCircleCI: HandleCircleCI = HandleCircleCI(packages=self._packages)
        handleCircleCI.update()

        echo('Update requirements.txt', color=True)
        hrt: HandleRequirementsTxt = HandleRequirementsTxt(packages=self._packages)
        hrt.update()

    def _buildPackagesToUpdate(self, specification: PyPath) -> Packages:
        with open(specification) as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            packages: Packages = Packages([])

            for row in csvreader:
                echo((row['PackageName'], row['OldVersion'], row['NewVersion']))
                packageName: PackageName = PackageName(row['PackageName'])
                updatePackage: UpdatePackage = UpdatePackage()
                updatePackage.packageName = packageName
                updatePackage.oldVersion = SemanticVersion(row['OldVersion'])
                updatePackage.newVersion = SemanticVersion(row['NewVersion'])
                packages.append(updatePackage)

        return packages


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('--specification', '-s', is_flag=False, flag_value='versionSpecification.csv', default='versionSpecification.csv',
        type=Path(exists=True, path_type=PyPath),
        required=False,
        help='Update the project using a specification file')
def commandHandler(specification: PyPath):
    """
    This command uses the .csv file created by createSpec
    """
    setUpLogging()
    vUpdate: VUpdate = VUpdate(specification=specification)
    vUpdate.update()
    # with open(specification) as csvfile:
    #     csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    #     packages: Packages = Packages([])
    #
    #     for row in csvreader:
    #         echo((row['PackageName'], row['OldVersion'], row['NewVersion']))
    #         packageName:   PackageName = PackageName(row['PackageName'])
    #         updatePackage: UpdatePackage = UpdatePackage()
    #         updatePackage.packageName = packageName
    #         updatePackage.oldVersion = SemanticVersion(row['OldVersion'])
    #         updatePackage.newVersion = SemanticVersion(row['NewVersion'])
    #         packages.append(updatePackage)
    #
    #     echo('Update setup.py', color=True)
    #     hsp: HandleSetupPy = HandleSetupPy(packages=packages)
    #     hsp.update()
    #
    #     echo('Update config.yml', color=True)
    #     handleCircleCI: HandleCircleCI = HandleCircleCI(packages=packages)
    #     handleCircleCI.update()
    #
    #     echo('Update requirements.txt', color=True)
    #     hrt: HandleRequirementsTxt = HandleRequirementsTxt(packages=packages)
    #     hrt.update()


if __name__ == "__main__":
    commandHandler()
