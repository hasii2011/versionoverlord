from pathlib import Path
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from tests.TestBase import TestBase
from versionoverlord.Common import AdvancedSlugs
from versionoverlord.FileNameToSlugs import FileNameToSlugs


class TestFileToAdvancedSlugs(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSimpleSlugs(self):
        """
        Slug name matches package name
        """
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'SimpleSlugs.slg')

        fileNameToSlugs: FileNameToSlugs = FileNameToSlugs(Path(fqFileName))

        advancedSlugs: AdvancedSlugs = fileNameToSlugs.getSlugs()

        for advancedSlug in advancedSlugs:
            if advancedSlug.slug == 'hasii2011/pyutmodel':
                self.assertEqual(advancedSlug.packageName, 'pyutmodel')
            if advancedSlug.slug == 'hasii2011/ogl':
                self.assertEqual(advancedSlug.packageName, 'ogl')
            if advancedSlug.slug == 'hasii2011/oglio':
                self.assertEqual(advancedSlug.packageName, 'oglio')

    def testAdvancedSlugs(self):
        """
        Slug name and package name are not the same
        """
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'AdvancedSlugs.slg')

        fileNameToSlugs: FileNameToSlugs = FileNameToSlugs(Path(fqFileName))

        advancedSlugs: AdvancedSlugs = fileNameToSlugs.getSlugs()

        for advancedSlug in advancedSlugs:
            if advancedSlug.slug == 'hasii2011/code-ally-advanced':
                self.assertEqual(advancedSlug.packageName, 'codeallyadvanced')
            if advancedSlug.slug == 'hasii2011/code-ally-basic':
                self.assertEqual(advancedSlug.packageName, 'codeallybasic')


def suite() -> TestSuite:
    """
    You need to change the name of the test class here also.
    """
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestFileToAdvancedSlugs))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
