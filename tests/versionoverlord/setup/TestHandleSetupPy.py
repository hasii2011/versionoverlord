
from typing import cast

from logging import Logger
from logging import getLogger

from os import unsetenv as osUnsetenv
from os import environ as osEnviron

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase
from versionoverlord.Common import ENV_PROJECT
from versionoverlord.Common import ENV_PROJECTS_BASE

from versionoverlord.exceptions.ProjectNotSetException import ProjectNotSetException
from versionoverlord.exceptions.ProjectsBaseNotSetException import ProjectsBaseNotSetException

from versionoverlord.setup.HandleSetupPy import HandleSetupPy


class TestHandleSetupPy(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestHandleSetupPy.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestHandleSetupPy.clsLogger

    def tearDown(self):
        pass

    def testProjectBaseNoteSet(self):
        self.assertRaises(ProjectsBaseNotSetException, lambda: self._failsOnProjectsBaseNotSet())

    def testProjectNotSet(self):
        self.assertRaises(ProjectNotSetException, lambda: self._failsOnProjectNotSet())

    def _failsOnProjectsBaseNotSet(self):
        try:
            del osEnviron[ENV_PROJECTS_BASE]
        except KeyError:
            pass    # May or may not exist;  don't care

        # noinspection PyUnusedLocal
        hsp: HandleSetupPy = HandleSetupPy()

    def _failsOnProjectNotSet(self):
        osEnviron[ENV_PROJECTS_BASE] = 'IAmFakeSet'
        del osEnviron[ENV_PROJECT]

        # noinspection PyUnusedLocal
        hsp: HandleSetupPy = HandleSetupPy()


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
