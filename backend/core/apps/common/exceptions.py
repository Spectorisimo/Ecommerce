from dataclasses import dataclass


@dataclass(eq=False)
class ServiceException(Exception):
    @property
    def message(self):
        return 'Application exception occurred'


@dataclass(eq=False)
class RepositoryException(Exception):
    @property
    def message(self):
        return 'Repository exception occurred'
