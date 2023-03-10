
from typing import cast

from logging import Logger
from logging import getLogger

from shutil import copy as shellCopy

from os import environ as osEnviron


from pathlib import Path

from pkg_resources import resource_filename

from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE
from versionoverlord.Common import Packages
from versionoverlord.Common import SETUP_PY

from versionoverlord.exceptions.NoSetupPyFileException import NoSetupPyFileException
from versionoverlord.exceptions.ProjectNotSetException import ProjectNotSetException
from versionoverlord.exceptions.ProjectsBaseNotSetException import ProjectsBaseNotSetException

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase
from versionoverlord.setup.HandleSetupPy import HandleSetupPy


class TestHandleSetupPy(TestBase):
    UNIT_TESTS_PROJECTS_BASE:      str = '/Users/humberto.a.sanchez.ii/PycharmProjects/'
    UNIT_TEST_PROJECT_NO_SETUP_PY: str = 'OverLordUnitTestNoSetupPy'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestHandleSetupPy.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestHandleSetupPy.clsLogger

        super().setUp()

        self._tmpNoSetupProjectDir:  Path = self._tmpProjectsBase / Path(TestHandleSetupPy.UNIT_TEST_PROJECT_NO_SETUP_PY)
        self._tmpNoSetupProjectDir.mkdir()

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, SETUP_PY)

        testSetupPyPath:      Path = Path(fqFileName)
        destinationSetupPyPath: Path = self._tmpProjectDir / Path(SETUP_PY)

        shellCopy(testSetupPyPath, destinationSetupPyPath)

        self.logger.debug(f'Projects Base: {self._tmpProjectsBase}')
        self.logger.debug(f'Project  Dir:  {self._tmpProjectDir}')
        self.logger.debug(f'No setup Dir:  {self._tmpNoSetupProjectDir}')

        self._destinationSetupPyPath: Path = destinationSetupPyPath

    def tearDown(self):
        self._destinationSetupPyPath.unlink(missing_ok=True)
        self._tmpNoSetupProjectDir.rmdir()
        self._tmpProjectDir.rmdir()

    def testProjectBaseNoteSet(self):
        self.assertRaises(ProjectsBaseNotSetException, lambda: self._failsOnProjectsBaseNotSet())

    def testProjectNotSet(self):
        self.assertRaises(ProjectNotSetException, lambda: self._failsOnProjectNotSet())

    def testUpdateNoSetupPy(self):
        self.assertRaises(NoSetupPyFileException, lambda: self._failsOnNoSetupPy())

    def testUpdate(self):

        osEnviron[ENV_PROJECTS_BASE] = self._tmpProjectsBase.__str__()
        osEnviron[ENV_PROJECT]       = self._tmpProjectDir.name

        hsp: HandleSetupPy = HandleSetupPy(packages=TestBase.TEST_PACKAGES)

        hsp.update()

        generatedFileName: Path = self._tmpProjectDir / Path(SETUP_PY)
        status: int = TestBase.runDiff(goldenFilename=SETUP_PY,
                                       generatedFileName=generatedFileName
                                       )

        self.assertEqual(0, status, 'setup.py not correctly updated')

    def _failsOnProjectsBaseNotSet(self):
        try:
            del osEnviron[ENV_PROJECTS_BASE]
        except KeyError:
            pass    # May or may not exist;  don't care

        # noinspection PyUnusedLocal
        hsp: HandleSetupPy = HandleSetupPy(Packages([]))

    def _failsOnProjectNotSet(self):
        osEnviron[ENV_PROJECTS_BASE] = self._tmpProjectsBase.__str__()
        try:
            del osEnviron[ENV_PROJECT]
        except KeyError:
            pass    # May or may not exist;  don't care

        # noinspection PyUnusedLocal
        hsp: HandleSetupPy = HandleSetupPy(Packages([]))

    def _failsOnNoSetupPy(self):
        osEnviron[ENV_PROJECTS_BASE] = self._tmpProjectsBase.__str__()
        osEnviron[ENV_PROJECT]       = self._tmpNoSetupProjectDir.name
        hsp: HandleSetupPy = HandleSetupPy(Packages([]))

        hsp.update()


def suite() -> TestSuite:
    """
    """
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences

    # testSuite.addTest(unittest.makeSuite(TestTemplate))
    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestHandleSetupPy))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
