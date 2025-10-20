# apps/dashboards/services/dashboard_service.py
from typing import Dict, List
from datetime import datetime, timedelta
from core.integrations.github_client import GitHubClient, GitHubAPIAdapter
from core.repositories.contributor_repository import ContributorRepository
from core.repositories.repo_repository import RepositoryRepository
from .dashboard_factory import DashboardFactory


class DashboardService:
    """
    Service Layer - Dashboard Business Logic
    Orchestrates data fetching, processing, and dashboard generation
    """

    def __init__(self, access_token: str):
        self.github_client = GitHubClient(access_token)
        self.adapter = GitHubAPIAdapter()
        self.contributor_repo = ContributorRepository()
        self.repo_repository = RepositoryRepository()

    def sync_repository_data(self, owner: str, repo: str) -> Dict:
        """Fetch and sync repository data from GitHub"""
        # Get repository info
        repo_data = self.github_client.get_repository(owner, repo)
        adapted_repo = self.adapter.adapt_repository(repo_data)

        # Store in MongoDB
        full_name = f"{owner}/{repo}"
        stored_repo = self.repo_repository.upsert_repository(full_name, adapted_repo)

        # Get and store contributors
        contributors = self.github_client.get_contributors(owner, repo)
        adapted_contributors = [self.adapter.adapt_contributor(c) for c in contributors]

        for contributor in adapted_contributors:
            contributor['repository'] = full_name

        self.contributor_repo.bulk_upsert(adapted_contributors)

        return stored_repo

    def generate_contributor_dashboard(self, owner: str, repo: str, username: str) -> Dict:
        """Generate comprehensive dashboard for a specific contributor"""
        # Fetch data from GitHub API
        commits = self.github_client.get_commits(owner, repo, author=username)
        issues = self.github_client.get_issues(owner, repo, creator=username)
        pull_requests = self.github_client.get_pull_requests(owner, repo, creator=username)
        recent_activity = self.github_client.get_user_activity(username)

        # Adapt data
        adapted_commits = [self.adapter.adapt_commit(c) for c in commits]
        adapted_issues = [self.adapter.adapt_issue(i) for i in issues]
        adapted_prs = [self.adapter.adapt_pull_request(pr) for pr in pull_requests]

        # Calculate metrics
        metrics = self._calculate_metrics(adapted_commits, adapted_issues, adapted_prs)

        # Generate charts data
        charts_data = self._generate_charts_data(adapted_commits, adapted_issues, adapted_prs)

        # Use Factory to create dashboard object
        dashboard = DashboardFactory.create_contributor_dashboard(
            username=username,
            repository=f"{owner}/{repo}",
            metrics=metrics,
            charts=charts_data,
            recent_activity=recent_activity[:10]
        )

        # Store in MongoDB
        self.contributor_repo.upsert_contributor(username, f"{owner}/{repo}", dashboard)

        return dashboard

    def generate_all_contributors_dashboards(self, owner: str, repo: str) -> List[Dict]:
        """Generate dashboards for all contributors in a repository"""
        contributors = self.github_client.get_contributors(owner, repo)
        dashboards = []

        for contributor in contributors:
            username = contributor.get('login')
            try:
                dashboard = self.generate_contributor_dashboard(owner, repo, username)
                dashboards.append(dashboard)
            except Exception as e:
                continue

        return dashboards

    def _calculate_metrics(self, commits: List[Dict], issues: List[Dict], prs: List[Dict]) -> Dict:
        """Calculate contributor metrics"""
        total_commits = len(commits)
        total_additions = sum(c['stats']['additions'] for c in commits)
        total_deletions = sum(c['stats']['deletions'] for c in commits)

        issues_opened = len([i for i in issues if i['state'] == 'open'])
        issues_closed = len([i for i in issues if i['state'] == 'closed'])

        prs_submitted = len(prs)
        prs_merged = len([pr for pr in prs if pr.get('merged', False)])
        prs_open = len([pr for pr in prs if pr['state'] == 'open'])

        return {
            'commits': {
                'total': total_commits,
                'additions': total_additions,
                'deletions': total_deletions,
                'net_change': total_additions - total_deletions,
            },
            'issues': {
                'total': len(issues),
                'opened': issues_opened,
                'closed': issues_closed,
                'close_rate': (issues_closed / len(issues) * 100) if issues else 0,
            },
            'pull_requests': {
                'total': prs_submitted,
                'merged': prs_merged,
                'open': prs_open,
                'merge_rate': (prs_merged / prs_submitted * 100) if prs_submitted else 0,
            },
        }

    def _generate_charts_data(self, commits: List[Dict], issues: List[Dict], prs: List[Dict]) -> Dict:
        """Generate data formatted for charts"""
        # Commits over time
        commits_timeline = self._group_by_date(commits, 'author.date')

        # Code changes distribution
        code_changes = [
            {
                'name': 'Additions',
                'value': sum(c['stats']['additions'] for c in commits)
            },
            {
                'name': 'Deletions',
                'value': sum(c['stats']['deletions'] for c in commits)
            }
        ]

        # Issues status
        issues_status = [
            {'name': 'Open', 'value': len([i for i in issues if i['state'] == 'open'])},
            {'name': 'Closed', 'value': len([i for i in issues if i['state'] == 'closed'])},
        ]

        # PRs status
        prs_status = [
            {'name': 'Merged', 'value': len([pr for pr in prs if pr.get('merged', False)])},
            {'name': 'Open', 'value': len([pr for pr in prs if pr['state'] == 'open'])},
            {'name': 'Closed',
             'value': len([pr for pr in prs if pr['state'] == 'closed' and not pr.get('merged', False)])},
        ]

        return {
            'commits_timeline': commits_timeline,
            'code_changes': code_changes,
            'issues_status': issues_status,
            'prs_status': prs_status,
        }

    def _group_by_date(self, items: List[Dict], date_field: str) -> List[Dict]:
        """Group items by date for timeline charts"""
        from collections import defaultdict
        grouped = defaultdict(int)

        for item in items:
            # Navigate nested fields
            date_value = item
            for field in date_field.split('.'):
                date_value = date_value.get(field, '')

            if date_value:
                date = datetime.fromisoformat(date_value.replace('Z', '+00:00')).date()
                grouped[str(date)] += 1

        return [{'date': date, 'count': count} for date, count in sorted(grouped.items())]


# apps/dashboards/services/dashboard_factory.py
from typing import Dict, List
from datetime import datetime


class DashboardFactory:
    """
    Factory Pattern - Creates standardized dashboard objects
    """

    @staticmethod
    def create_contributor_dashboard(
            username: str,
            repository: str,
            metrics: Dict,
            charts: Dict,
            recent_activity: List[Dict]
    ) -> Dict:
        """Factory method to create a contributor dashboard"""
        return {
            'username': username,
            'repository': repository,
            'generated_at': datetime.utcnow().isoformat(),
            'metrics': metrics,
            'charts': charts,
            'recent_activity': recent_activity,
            'summary': DashboardFactory._generate_summary(metrics),
        }

    @staticmethod
    def _generate_summary(metrics: Dict) -> Dict:
        """Generate a summary of key statistics"""
        return {
            'total_contributions': (
                    metrics['commits']['total'] +
                    metrics['issues']['total'] +
                    metrics['pull_requests']['total']
            ),
            'productivity_score': DashboardFactory._calculate_productivity_score(metrics),
            'engagement_level': DashboardFactory._calculate_engagement_level(metrics),
        }

    @staticmethod
    def _calculate_productivity_score(metrics: Dict) -> float:
        """Calculate a productivity score (0-100)"""
        commits = metrics['commits']['total']
        prs_merged = metrics['pull_requests']['merged']
        issues_closed = metrics['issues']['closed']

        # Weighted scoring
        score = (commits * 1) + (prs_merged * 5) + (issues_closed * 3)
        return min(score, 100)

    @staticmethod
    def _calculate_engagement_level(metrics: Dict) -> str:
        """Determine engagement level based on activity"""
        total = metrics['commits']['total'] + metrics['issues']['total'] + metrics['pull_requests']['total']

        if total >= 50:
            return 'High'
        elif total >= 20:
            return 'Medium'
        elif total > 0:
            return 'Low'
        else:
            return 'Inactive'