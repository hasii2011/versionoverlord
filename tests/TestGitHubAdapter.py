
from unittest import TestSuite
from unittest import main as unitTestMain

from semantic_version import Version as SemanticVersion

from tests.TestBase import TestBase

from versionoverlord.Common import RepositorySlug

from versionoverlord.GitHubAdapter import GitHubAdapter
from versionoverlord.GitHubAdapterTypes import AdapterMilestone
from versionoverlord.GitHubAdapterTypes import AdapterRelease
from versionoverlord.githubadapter.exceptions.GitHubAdapterError import GitHubAdapterError
from versionoverlord.githubadapter.exceptions.UnknownGitHubRelease import UnknownGitHubRelease

TEST_SLUG:        RepositorySlug  = RepositorySlug('hasii2011/TestRepository')
BOGUS_RELEASE_ID: int             = 6666
TEST_TAG:         SemanticVersion = SemanticVersion('10.0.0')

TEST_MILESTONE_TITLE: str = 'AdapterRelease 10.0.0'


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

        release: AdapterRelease = gitHubAdapter.createDraftRelease(repositorySlug=TEST_SLUG, tag=TEST_TAG)

        self.assertEqual(True, release.draft, 'Must be a draft release')
        # cleanup
        gitHubAdapter.deleteRelease(repositorySlug=TEST_SLUG, releaseId=release.id)

    def testCreateMilestone(self):
        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        try:
            adapterMilestone: AdapterMilestone = gitHubAdapter.createMilestone(repositorySlug=TEST_SLUG, title=TEST_MILESTONE_TITLE)
            self.assertEqual(TEST_MILESTONE_TITLE, adapterMilestone.title, 'Oops title mismatch')
            # clean up
            gitHubAdapter.deleteMilestone(repositorySlug=TEST_SLUG, releaseNumber=adapterMilestone.releaseNumber)
        except GitHubAdapterError as e:
            self.logger.error(f'{e.message}')
            self.fail('We should not get a failure')

    def testDeleteRelease(self):

        gitHubAdapter: GitHubAdapter = GitHubAdapter()
        release:       AdapterRelease       = gitHubAdapter.createDraftRelease(repositorySlug=TEST_SLUG, tag=TEST_TAG)

        gitHubAdapter.deleteRelease(repositorySlug=TEST_SLUG, releaseId=release.id)

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
