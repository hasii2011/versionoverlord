
import json

import logging
import logging.config

from os import system as osSystem

from pathlib import Path

from tempfile import gettempdir

from pkg_resources import resource_filename

from unittest import TestCase

from hasiicommon.SemanticVersion import SemanticVersion

from versionoverlord.Common import PackageName
from versionoverlord.Common import Packages
from versionoverlord.Common import UpdatePackage


JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:           str = 'tests.resources'
    RESOURCES_TEST_DATA_PACKAGE_NAME: str = f'{RESOURCES_PACKAGE_NAME}.testdata'
    GOLDEN_PACKAGE_NAME:              str = f'{RESOURCES_TEST_DATA_PACKAGE_NAME}.golden'

    EXTERNAL_DIFF:         str = '/usr/bin/diff -w '
    EXTERNAL_CLEAN_UP_TMP: str = 'rm -rf'

    TEST_PROJECTS_BASE: str = 'unitTestProjectsBase'
    UNIT_TEST_PROJECT:  str = 'OverLordUnitTest'

    TEST_PACKAGES: Packages = Packages(
        [
            UpdatePackage(packageName=PackageName('ogl'),      oldVersion=SemanticVersion('0.70.20'), newVersion=SemanticVersion('0.80.0')),
            UpdatePackage(packageName=PackageName('untangle'), oldVersion=SemanticVersion('1.2.1'),   newVersion=SemanticVersion('1.3.0'))
        ]
    )

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        tmpDir = gettempdir()
        tmpProjectsBase: Path = Path(tmpDir) / Path(TestBase.TEST_PROJECTS_BASE)
        tmpProjectsBase.mkdir(exist_ok=True)

        tmpProjectDir:   Path = tmpProjectsBase / Path(TestBase.UNIT_TEST_PROJECT)
        tmpProjectDir.mkdir(exist_ok=True)

        self._tmpProjectsBase: Path = tmpProjectsBase
        self._tmpProjectDir:   Path = tmpProjectDir

    def tearDown(self):
        """
        """
        "Hook method for deconstructing the test fixture after testing it."
        pass

    """
    A base unit test class to initialize some logging stuff we need
    """
    @classmethod
    def setUpLogging(cls):
        """"""
        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName

    @classmethod
    def runDiff(cls, goldenFilename: str, generatedFileName: Path) -> int:
        """
        Assumes the caller use our ._constructGeneratedName method to get
        a fully qualified file name

        Args:
            goldenFilename:     The base file name
            generatedFileName:  The Path object that represents a generated file name with updated contents

        Returns:  The results of the difference
        """
        goldenFileName:    str = resource_filename(TestBase.GOLDEN_PACKAGE_NAME, goldenFilename)

        status: int = osSystem(f'{TestBase.EXTERNAL_DIFF} {goldenFileName} {generatedFileName.__str__()}')

        return status
