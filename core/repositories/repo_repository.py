# core/repositories/repo_repository.py
# Minimal in-memory repository for repositories
from typing import Dict


class RepositoryRepository:
    _repos: Dict[str, Dict] = {}

    def upsert_repository(self, full_name: str, data: Dict) -> Dict:
        existing = self._repos.get(full_name, {})
        existing.update(data or {})
        # Ensure full_name is set
        if full_name:
            existing["full_name"] = full_name
        self._repos[full_name] = existing
        return existing
