
from typing import cast

from logging import Logger
from logging import getLogger

from pathlib import Path

from shutil import copy as shellCopy

from os import environ as osEnviron

from pkg_resources import resource_filename

from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE

from versionoverlord.Common import Packages
from versionoverlord.Common import REQUIREMENTS_TXT

from versionoverlord.exceptions.NoRequirementsTxtsException import NoRequirementsTxtException

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase
from versionoverlord.requirements.HandleRequirementsTxt import HandleRequirementsTxt


class TestHandleRequirementsTxt(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    UNIT_TEST_PROJECT_NO_REQUIREMENTS_TXT: str = 'OverLordUnitTestNoRequirementsTxt'

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestHandleRequirementsTxt.clsLogger = getLogger(__name__)

    def setUp(self):
        super().setUp()
        self.logger:             Logger = TestHandleRequirementsTxt.clsLogger
        self._tmpNoRequirementsTxtDir: Path = self._tmpProjectsBase / Path(TestHandleRequirementsTxt.UNIT_TEST_PROJECT_NO_REQUIREMENTS_TXT)
        self._tmpNoRequirementsTxtDir.mkdir()

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, REQUIREMENTS_TXT)

        testRequirementsTxtPath:       Path = Path(fqFileName)
        destinationRequirementsTxtPath: Path = self._tmpProjectDir / Path(REQUIREMENTS_TXT)

        self.logger.info(f'Copy to: {destinationRequirementsTxtPath}')
        shellCopy(testRequirementsTxtPath, destinationRequirementsTxtPath)

        self._destinationRequirementsTxtPath: Path = destinationRequirementsTxtPath

    def tearDown(self):
        self._destinationRequirementsTxtPath.unlink(missing_ok=True)
        self._tmpNoRequirementsTxtDir.rmdir()

    def testUpdateNoRequirementsTxt(self):
        self.assertRaises(NoRequirementsTxtException, lambda: self._failsOnNoRequirementsTxt())

    def testUpdate(self):

        osEnviron[ENV_PROJECTS_BASE] = self._tmpProjectsBase.__str__()
        osEnviron[ENV_PROJECT]       = self._tmpProjectDir.name

        hrt: HandleRequirementsTxt = HandleRequirementsTxt(packages=TestBase.TEST_PACKAGES)

        hrt.update()

        generatedFileName: Path = self._tmpProjectDir / Path(REQUIREMENTS_TXT)

        status: int = TestBase.runDiff(goldenFilename=REQUIREMENTS_TXT,
                                       generatedFileName=generatedFileName
                                       )

        self.assertEqual(0, status, 'requirements.txt not correctly updated')

    def _failsOnNoRequirementsTxt(self):
        osEnviron[ENV_PROJECTS_BASE] = self._tmpProjectsBase.__str__()
        osEnviron[ENV_PROJECT]       = self._tmpNoRequirementsTxtDir.name

        hrt: HandleRequirementsTxt = HandleRequirementsTxt(Packages([]))

        hrt.update()        # empty won't be used


def suite() -> TestSuite:
    """
    """
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    # testSuite.addTest(unittest.makeSuite(TestTemplate))
    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestHandleRequirementsTxt))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
