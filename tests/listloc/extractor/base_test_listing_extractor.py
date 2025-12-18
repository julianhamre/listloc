import unittest
import tempfile

from tests.listloc.extractor.file_creation_tools import FileCreationTools
from src.listloc.extractor.extractor_context import ExtractorContext
from src.listloc.extractor.listing_extractor import ListingExtractor

class BaseTestListingExtractor(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.TemporaryDirectory()
        self._BASE_DIRECTORY_PATH = self.__temp_dir.name

    def _create_test_file_structure(self, subdirs, files):
        self._SUBDIRS = subdirs
        self._FILES = files
        file_creator = FileCreationTools(self._BASE_DIRECTORY_PATH, self._SUBDIRS, self._FILES)
        file_creator.create_subdirs_and_code_files()
        self._context = ExtractorContext(self._BASE_DIRECTORY_PATH)
        self._listing_extractor = ListingExtractor(self._BASE_DIRECTORY_PATH, self._context)

    def tearDown(self):
        self.__temp_dir.cleanup()