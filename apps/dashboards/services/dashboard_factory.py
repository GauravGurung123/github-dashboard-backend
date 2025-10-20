# apps/dashboards/services/dashboard_factory.py
from typing import Dict, List


class DashboardFactory:
    """
    Simple factory to assemble dashboard objects.
    """

    @staticmethod
    def create_contributor_dashboard(
        username: str,
        repository: str,
        metrics: Dict,
        charts: Dict,
        recent_activity: List[Dict],
    ) -> Dict:
        return {
            "username": username,
            "repository": repository,
            "metrics": metrics or {},
            "charts": charts or {},
            "recent_activity": recent_activity or [],
            "generated": True,
        }
