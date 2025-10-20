# core/repositories/contributor_repository.py
# Minimal in-memory repository to satisfy service dependencies.
from typing import Dict, List


class ContributorRepository:
    _store: Dict[str, List[Dict]] = {}
    _dashboards: Dict[str, Dict] = {}

    def get_by_repository(self, full_repo_name: str) -> List[Dict]:
        return self._store.get(full_repo_name, [])

    def bulk_upsert(self, contributors: List[Dict]) -> None:
        # Group contributors by repository key
        by_repo: Dict[str, List[Dict]] = {}
        for c in contributors:
            repo = c.get("repository")
            if not repo:
                continue
            by_repo.setdefault(repo, [])
            # Upsert by login
            existing = {ec.get("login"): ec for ec in by_repo[repo]}
            login = c.get("login")
            if login in existing:
                existing[login].update(c)
            else:
                by_repo[repo].append(c)
        for repo, items in by_repo.items():
            self._store[repo] = items

    def upsert_contributor(self, username: str, repository: str, dashboard: Dict) -> None:
        key = f"{repository}:{username}"
        self._dashboards[key] = dashboard

    def get_dashboard(self, username: str, repository: str) -> Dict:
        key = f"{repository}:{username}"
        return self._dashboards.get(key, {})
