class GitHubServiceRequestException(Exception):
    pass


class CalculateScoreException(Exception):
    pass


class RepositoryNameException(Exception):
    pass


class RepositoryNotFoundException(Exception):
    pass


class RepositoryForbiddenException(Exception):
    pass


class RepositoryMovedPermanently(Exception):
    pass
