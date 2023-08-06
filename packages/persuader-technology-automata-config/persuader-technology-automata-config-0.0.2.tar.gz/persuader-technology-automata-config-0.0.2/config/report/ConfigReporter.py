from missingrepo.Missing import Missing
from missingrepo.repository.MissingRepository import MissingRepository


class ConfigReporter:

    def __init__(self, missing_repository: MissingRepository):
        self.missing_repository = missing_repository

    def report_missing(self, missing: Missing):
        self.missing_repository.store(missing)
