from listloc.extractor.context.action_logger import ActionLogger
from listloc.extractor.context.listing_name_logger import ListingNameLogger

class ExtractorContext:

    def __init__(self, base_directory_path, verbose=False):
        self.action_logger = ActionLogger(base_directory_path, verbose=verbose)
        self.listing_name_logger = ListingNameLogger()