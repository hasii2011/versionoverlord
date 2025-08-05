
from importlib.abc import Traversable
from importlib.resources import files

from pathlib import Path

from os import environ as osEnviron

from shutil import copy as shellCopy

from unittest import TestSuite
from unittest import main as unitTestMain

from versionoverlord.Common import CIRCLE_CI_DIRECTORY
from versionoverlord.Common import CIRCLE_CI_YAML
from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE

from versionoverlord.circleci.HandleCircleCI import HandleCircleCI

from tests.TestBase import TestBase


class TestHandleCircleCI(TestBase):
    """
    """
    keep:      bool   = False

    @classmethod
    def setUpClass(cls):

        TestBase.setUpClass()
        if 'KEEP' in osEnviron:
            keep: str = osEnviron["KEEP"]
            if keep.lower().strip() == 'true':
                cls.keep = True
            else:
                cls.keep = False
        else:
            print(f'No need to keep data files')
            cls.keep = False

    def setUp(self):
        super().setUp()

        self._circleCIPath: Path = self._tmpProjectDir / Path(CIRCLE_CI_DIRECTORY)
        self._circleCIPath.mkdir(exist_ok=True)
        self._destinationYamFilePath: Path = self._circleCIPath / Path(CIRCLE_CI_YAML)

    def tearDown(self):
        super().tearDown()
        # noinspection PySimplifyBooleanCheck
        if TestHandleCircleCI.keep is False:
            TestBase.deleteDirectory(self._tmpProjectsBase)

    def testUpdate(self):

        self._copyTestConfigFileToUnitTestProject()

        osEnviron[ENV_PROJECTS_BASE] = str(self._tmpProjectsBase)
        osEnviron[ENV_PROJECT]       = self._tmpProjectDir.name

        handleCircleCI: HandleCircleCI = HandleCircleCI(packages=TestBase.TEST_PACKAGES)

        handleCircleCI.update()

        status: int = TestBase.runDiff(goldenFilename=CIRCLE_CI_YAML,
                                       generatedFileName=self._destinationYamFilePath
                                       )

        self.assertEqual(0, status, 'config.yml not correctly updated')

        # cleanup
        # noinspection PySimplifyBooleanCheck
        if TestHandleCircleCI.keep is False:
            self._destinationYamFilePath.unlink()

    def _copyTestConfigFileToUnitTestProject(self):

        traversable: Traversable = files(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME) / CIRCLE_CI_YAML

        # testYamlFile:     str  = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, CIRCLE_CI_YAML)
        testYamlFile:     str = str(traversable)
        testYamlFilePath: Path = Path(testYamlFile)

        self.logger.debug(f'Copy to: {self._destinationYamFilePath}')
        shellCopy(testYamlFilePath, self._destinationYamFilePath)


def suite() -> TestSuite:
    """
    """
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    # testSuite.addTest(unittest.makeSuite(TestTemplate))
    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestHandleCircleCI))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
