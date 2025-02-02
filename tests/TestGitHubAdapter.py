
from unittest import TestSuite
from unittest import main as unitTestMain

from time import sleep as takeANap

from semantic_version import Version as SemanticVersion

from tests.TestBase import TestBase

from versionoverlord.Common import RepositorySlug

from versionoverlord.githubadapter.GitHubAdapter import GitHubAdapter
from versionoverlord.githubadapter.GitHubAdapterTypes import AdapterMilestone
from versionoverlord.githubadapter.GitHubAdapterTypes import AdapterRelease

from versionoverlord.githubadapter.exceptions.GitHubAdapterError import GitHubAdapterError

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

        release: AdapterRelease = gitHubAdapter.createDraftRelease(repositorySlug=TEST_SLUG, tag=TEST_TAG, message='')

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
        release:       AdapterRelease       = gitHubAdapter.createDraftRelease(repositorySlug=TEST_SLUG, tag=TEST_TAG, message='')

        gitHubAdapter.deleteRelease(repositorySlug=TEST_SLUG, releaseId=release.id)

    def testDeleteReleaseFail(self):

        gitHubAdapter: GitHubAdapter = GitHubAdapter()
        self.assertRaises(GitHubAdapterError, lambda: gitHubAdapter.deleteRelease(repositorySlug=TEST_SLUG, releaseId=BOGUS_RELEASE_ID))

    def testPublishRelease(self):
        """
        Put small delays because these sometime fail
        """

        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        release: AdapterRelease = gitHubAdapter.createDraftRelease(repositorySlug=TEST_SLUG, tag=TEST_TAG, message='')

        takeANap(1)
        gitHubAdapter.publishRelease(repositorySlug=TEST_SLUG, releaseTitle=release.title)
        takeANap(1)
        # cleanup
        gitHubAdapter.deleteRelease(repositorySlug=TEST_SLUG, releaseId=release.id)


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
