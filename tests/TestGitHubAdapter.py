
from unittest import TestSuite
from unittest import main as unitTestMain

from semantic_version import Version as SemanticVersion

from tests.TestBase import TestBase

from versionoverlord.GitHubAdapter import GitHubAdapter


class TestGitHubAdapter(TestBase):
    """
    """
    def setUp(self):
        super().setUp()
        """
            I don't care about:
            
                DeprecationWarning: Argument login_or_token is deprecated, please use auth=github.Auth.Token(...) instead
        """
        import warnings

        warnings.filterwarnings(action="ignore", message="Argument", category=DeprecationWarning)

    def tearDown(self):
        pass

    def testBasic(self):
        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        version: SemanticVersion = gitHubAdapter.getLatestVersionNumber('hasii2011/hasiicommon')
        self.assertNotEqual(None, version, 'Something wrong should not be None')
        self.assertNotEqual('', version,   'Something wrong should not be Empty')
        self.logger.info(f'{version}')


def suite() -> TestSuite:
    """
    You need to change the name of the test class here also.
    """
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGitHubAdapter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
