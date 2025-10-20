# core/integrations/github_client.py
# Minimal GitHub API client and adapter to satisfy imports and allow the server to run.
# These are lightweight placeholders and can be expanded to call the real GitHub API.
from typing import Dict, List, Optional


class GitHubClient:
    """
    Minimal stub GitHub client. In a real implementation this would call GitHub's REST API
    using the provided access token.
    """

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or ""

    # User-level data
    def get_user_repositories(self) -> List[Dict]:
        # Return an empty list for now; structure matches expected adapter input
        return []

    def get_user_activity(self, username: str) -> List[Dict]:
        return []

    # Repository-level data
    def get_repository(self, owner: str, repo: str) -> Dict:
        return {"full_name": f"{owner}/{repo}", "name": repo, "owner": {"login": owner}}

    def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        return []

    def get_commits(self, owner: str, repo: str, author: Optional[str] = None) -> List[Dict]:
        return []

    def get_issues(self, owner: str, repo: str, creator: Optional[str] = None) -> List[Dict]:
        return []

    def get_pull_requests(self, owner: str, repo: str, creator: Optional[str] = None) -> List[Dict]:
        return []


class GitHubAPIAdapter:
    """
    Adapts raw GitHub API responses to simplified internal representations.
    """

    def __init__(self):
        pass

    def adapt_repository(self, repo: Dict) -> Dict:
        if not repo:
            return {}
        return {
            "id": repo.get("id"),
            "name": repo.get("name"),
            "full_name": repo.get("full_name") or (
                f"{repo.get('owner', {}).get('login','')}/{repo.get('name','')}" if repo.get("name") else None
            ),
            "owner": repo.get("owner", {}).get("login"),
            "private": repo.get("private", False),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
        }

    def adapt_contributor(self, contributor: Dict) -> Dict:
        if not contributor:
            return {}
        return {
            "id": contributor.get("id"),
            "login": contributor.get("login"),
            "contributions": contributor.get("contributions", 0),
            "avatar_url": contributor.get("avatar_url"),
            "html_url": contributor.get("html_url"),
        }

    def adapt_commit(self, commit: Dict) -> Dict:
        if not commit:
            return {"stats": {"additions": 0, "deletions": 0}, "author": {"date": None}}
        stats = commit.get("stats") or {}
        commit_info = commit.get("commit") or {}
        author_info = commit_info.get("author") or {}
        return {
            "sha": commit.get("sha"),
            "message": commit_info.get("message"),
            "stats": {
                "additions": stats.get("additions", 0),
                "deletions": stats.get("deletions", 0),
            },
            "author": {
                "date": author_info.get("date"),
                "name": author_info.get("name"),
            },
        }

    def adapt_issue(self, issue: Dict) -> Dict:
        if not issue:
            return {"state": "open"}
        return {
            "id": issue.get("id"),
            "title": issue.get("title"),
            "state": issue.get("state", "open"),
            "created_at": issue.get("created_at"),
            "closed_at": issue.get("closed_at"),
            "user": (issue.get("user") or {}).get("login"),
        }

    def adapt_pull_request(self, pr: Dict) -> Dict:
        if not pr:
            return {"state": "open", "merged": False}
        return {
            "id": pr.get("id"),
            "title": pr.get("title"),
            "state": pr.get("state", "open"),
            "merged": pr.get("merged", False),
            "created_at": pr.get("created_at"),
            "merged_at": pr.get("merged_at"),
            "user": (pr.get("user") or {}).get("login"),
        }
