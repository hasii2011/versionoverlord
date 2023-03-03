from pathlib import Path
from typing import cast

from logging import Logger
from logging import getLogger

from os import environ as osEnviron

from shutil import copy as shellCopy

from unittest import TestSuite
from unittest import main as unitTestMain

from pkg_resources import resource_filename

from versionoverlord.Common import CIRCLE_CI_DIRECTORY
from versionoverlord.Common import CIRCLE_CI_YAML
from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE
from versionoverlord.Common import Packages
from versionoverlord.circleci.HandleCircleCI import HandleCircleCI
from versionoverlord.exceptions.NotACircleCIProjectException import NotACircleCIProjectException

from tests.TestBase import TestBase


class TestHandleCircleCI(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)
    keep:      bool   = False

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestHandleCircleCI.clsLogger = getLogger(__name__)

        if 'KEEP' in osEnviron:
            keep: str = osEnviron["KEEP"]
            if keep.lower().strip() == 'true':
                cls.keep = True
            else:
                cls.keep = False
        else:
            cls.clsLogger.info(f'No need to keep data files')
            cls.keep = False

    def setUp(self):
        super().setUp()
        self.logger: Logger = TestHandleCircleCI.clsLogger

        self._circleCIPath: Path = self._tmpProjectDir / Path(CIRCLE_CI_DIRECTORY)
        self._circleCIPath.mkdir(exist_ok=True)
        self._destinationYamFilePath: Path = self._circleCIPath / Path(CIRCLE_CI_YAML)

    def tearDown(self):
        if TestHandleCircleCI.keep is False:
            self._circleCIPath.rmdir()
            self._tmpProjectDir.rmdir()
            self._tmpProjectsBase.rmdir()

    def testNotACircleCIProject(self):
        self.assertRaises(NotACircleCIProjectException, lambda: self._failsNotACircleCIProject())

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
        if TestHandleCircleCI.keep is False:
            self._destinationYamFilePath.unlink()

    def _failsNotACircleCIProject(self):
        osEnviron[ENV_PROJECTS_BASE] = str(self._tmpProjectsBase)
        osEnviron[ENV_PROJECT]       = self._tmpProjectDir.name

        self.logger.debug(f'In: _failsNotACircleCIProject')
        handleCircleCI: HandleCircleCI = HandleCircleCI(packages=Packages([]))

        handleCircleCI.update()

    def _copyTestConfigFileToUnitTestProject(self):

        testYamlFile:     str  = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, CIRCLE_CI_YAML)
        testYamlFilePath: Path = Path(testYamlFile)

        self.logger.info(f'Copy to: {self._destinationYamFilePath}')
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
