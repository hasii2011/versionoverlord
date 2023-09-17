
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.SemanticVersion import SemanticVersion

from tests.TestBase import TestBase

from versionoverlord.GitHubAdapter import GitHubAdapter


class TestGitHubAdapter(TestBase):
    """
    """
    def setUp(self):
        super().setUp()

    # noinspection SpellCheckingInspection
    """
        I don't care about:
            ResourceWarning: unclosed <ssl.SSLSocket fd=8, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, 
            laddr=('192.168.0.24', 51944), raddr=('140.82.112.5', 443)>
    """

    import warnings
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

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
    # noinspection PyUnresolvedReferences
    # testSuite.addTest(unittest.makeSuite(TestTemplate))
    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGitHubAdapter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
