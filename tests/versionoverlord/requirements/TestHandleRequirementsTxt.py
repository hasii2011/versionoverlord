
from pathlib import Path

from shutil import copy as shellCopy

from os import environ as osEnviron

from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE

from versionoverlord.Common import REQUIREMENTS_TXT

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase
from versionoverlord.requirements.HandleRequirementsTxt import HandleRequirementsTxt


class TestHandleRequirementsTxt(TestBase):
    """
    """
    UNIT_TEST_PROJECT_NO_REQUIREMENTS_TXT: str = 'OverLordUnitTestNoRequirementsTxt'

    def setUp(self):
        super().setUp()

        self._tmpNoRequirementsTxtDir: Path = self._tmpProjectsBase / Path(TestHandleRequirementsTxt.UNIT_TEST_PROJECT_NO_REQUIREMENTS_TXT)
        self._tmpNoRequirementsTxtDir.mkdir()

        fqFileName: str = self.getFullyQualifiedResourceFileName(package=TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, fileName=REQUIREMENTS_TXT)

        testRequirementsTxtPath:        Path = Path(fqFileName)
        destinationRequirementsTxtPath: Path = self._tmpProjectDir / Path(REQUIREMENTS_TXT)

        self.logger.info(f'Copy to: {destinationRequirementsTxtPath}')
        shellCopy(testRequirementsTxtPath, destinationRequirementsTxtPath)

        self._destinationRequirementsTxtPath: Path = destinationRequirementsTxtPath

    def tearDown(self):
        self._destinationRequirementsTxtPath.unlink(missing_ok=True)
        self._tmpNoRequirementsTxtDir.rmdir()

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
