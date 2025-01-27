
from unittest import TestSuite
from unittest import main as unitTestMain

from semantic_version import Version as SemanticVersion

from github.GitRelease import GitRelease

from tests.TestBase import TestBase

from versionoverlord.Common import RepositorySlug

from versionoverlord.GitHubAdapter import GitHubAdapter
from versionoverlord.exceptions.UnknownGitHubRelease import UnknownGitHubRelease

TEST_SLUG:        RepositorySlug  = RepositorySlug('hasii2011/TestRepository')
BOGUS_RELEASE_ID: int             = 6666
TEST_TAG:         SemanticVersion = SemanticVersion('10.0.0')


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

        version: SemanticVersion = gitHubAdapter.getLatestVersionNumber(TEST_SLUG)
        self.assertNotEqual(None, version, 'Something wrong should not be None')
        self.assertNotEqual('', version,   'Something wrong should not be Empty')
        self.logger.info(f'{version}')

    def testCreateDraftRelease(self):

        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        gitRelease: GitRelease = gitHubAdapter.createDraftRelease(repositorySlug=TEST_SLUG, tag=TEST_TAG)

        self.assertEqual(True, gitRelease.draft, 'Must be a draft release')
        # cleanup
        gitRelease.delete_release()

    def testDeleteRelease(self):

        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        gitRelease: GitRelease = gitHubAdapter.createDraftRelease(repositorySlug=TEST_SLUG, tag=TEST_TAG)

        gitHubAdapter.deleteRelease(repositorySlug=TEST_SLUG, releaseId=gitRelease.id)


    def testDeleteReleaseFail(self):

        gitHubAdapter: GitHubAdapter = GitHubAdapter()
        self.assertRaises(UnknownGitHubRelease, lambda: gitHubAdapter.deleteRelease(repositorySlug=TEST_SLUG, releaseId=BOGUS_RELEASE_ID))


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
