
from os import environ as osEnviron

from pathlib import Path

from shutil import copy as shellCopy

from semantic_version import Version as SemanticVersion

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase
from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE
from versionoverlord.Common import PYPROJECT_TOML
from versionoverlord.Common import PackageName
from versionoverlord.Common import Packages
from versionoverlord.Common import UpdatePackage
from versionoverlord.pyprojecttoml.HandlePyProjectToml import HandlePyProjectToml


# import the class you want to test here
# from org.pyut.template import template


class TestHandlePyProjectToml(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx` is the name of the class that you want to test.

    See existing tests for more information.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

        fqTestFileName:         str = self.getFullyQualifiedResourceFileName(package=TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, fileName=PYPROJECT_TOML)
        testPyProjectTomlPath:  Path = Path(fqTestFileName)

        self._tmpPyProjectTomlPath: Path = self._tmpProjectDir / Path(PYPROJECT_TOML)

        self.logger.info(f'Copy to: {self._tmpPyProjectTomlPath}')

        shellCopy(testPyProjectTomlPath, self._tmpPyProjectTomlPath)

        self._packages: Packages = Packages(
            [
                UpdatePackage(packageName=PackageName('codeallybasic'), oldVersion=SemanticVersion('0.5.2'), newVersion=SemanticVersion('0.80.0')),
                UpdatePackage(packageName=PackageName('Deprecated'),    oldVersion=SemanticVersion('1.2.4'), newVersion=SemanticVersion('1.3.0'))
            ]
        )

    def tearDown(self):
        super().tearDown()
        self._tmpPyProjectTomlPath.unlink(missing_ok=True)
        self._tmpProjectDir.rmdir()

    def testBasic(self):

        osEnviron[ENV_PROJECTS_BASE] = self._tmpProjectsBase.__str__()
        osEnviron[ENV_PROJECT]       = self._tmpProjectDir.name

        tomlHandler: HandlePyProjectToml = HandlePyProjectToml(packages=self._packages)

        tomlHandler.update()

        status: int = TestBase.runDiff(goldenFilename=PYPROJECT_TOML,
                                       generatedFileName=self._tmpPyProjectTomlPath
                                       )

        self.assertEqual(0, status, 'pyproject.tom not correctly updated')

    def testNotFound(self):

        self._tmpPyProjectTomlPath.unlink()

        osEnviron[ENV_PROJECTS_BASE] = self._tmpProjectsBase.__str__()
        osEnviron[ENV_PROJECT]       = self._tmpProjectDir.name

        tomlHandler: HandlePyProjectToml = HandlePyProjectToml(packages=self._packages)

        self.assertFalse(tomlHandler.configurationExists, 'The configuration files does not exist')


def suite() -> TestSuite:
    """
    You need to change the name of the test class here also.
    """
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestHandlePyProjectToml))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
