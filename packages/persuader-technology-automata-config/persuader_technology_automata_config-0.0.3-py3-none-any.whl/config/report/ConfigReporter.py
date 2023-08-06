from missingrepo.Missing import Missing
from missingrepo.repository.MissingRepository import MissingRepository


class ConfigReporter:

    def __init__(self, missing_repository: MissingRepository):
        self.missing_repository = missing_repository
        self.ignored_check_func = None

    def set_ignored_check_func(self, func):
        self.ignored_check_func = func

    def report_missing(self, missing: Missing, func=None):
        if self.is_already_ignored(missing) or self.missing_repository.is_already_missing(missing):
            return
        self.missing_repository.store(missing)
        if func is not None:
            func()

    def is_already_ignored(self, missing: Missing) -> bool:
        return False if self.ignored_check_func is None else self.ignored_check_func(missing)
