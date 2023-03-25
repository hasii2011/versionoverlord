
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from hasiicommon.SemanticVersion import SemanticVersion

from tests.TestBase import TestBase
from versionoverlord.GitHubAdapter import GitHubAdapter


class TestGitHubAdapter(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGitHubAdapter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestGitHubAdapter.clsLogger

    def tearDown(self):
        pass

    def testBasic(self):
        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        version: SemanticVersion = gitHubAdapter.getLatestVersionNumber('hasii2011/hasiicommon')
        self.logger.info(f'{version}')


def suite() -> TestSuite:
    """
    You need to change the name of the test class here also.
    """
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    # testSuite.addTest(unittest.makeSuite(TestTemplate))
    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGitHubAdapter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
