class GitHubAPIException(Exception):
    """Custom exception for GitHub API errors"""
    pass


class RepositoryNotFoundException(Exception):
    """Repository not found exception"""
    pass


class ContributorNotFoundException(Exception):
    """Contributor not found exception"""
    pass