# core/repositories/base_repository.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pymongo import MongoClient
from django.conf import settings


class BaseRepository(ABC):
    """
    Abstract Base Repository - Repository Pattern
    Provides interface for data access operations
    """

    def __init__(self, collection_name: str):
        self.client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        self.db = self.client[settings.DATABASES['default']['NAME']]
        self.collection = self.db[collection_name]

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Dict]:
        """Retrieve a single document by ID"""
        pass

    @abstractmethod
    def get_all(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Retrieve all documents matching filters"""
        pass

    @abstractmethod
    def create(self, data: Dict) -> Dict:
        """Create a new document"""
        pass

    @abstractmethod
    def update(self, id: str, data: Dict) -> bool:
        """Update an existing document"""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete a document"""
        pass


# core/repositories/contributor_repository.py
from typing import Dict, List, Optional
from bson import ObjectId
from datetime import datetime
from .base_repository import BaseRepository


class ContributorRepository(BaseRepository):
    """
    Contributor Repository - Manages contributor data in MongoDB
    """

    def __init__(self):
        super().__init__('contributors')

    def get_by_id(self, id: str) -> Optional[Dict]:
        """Get contributor by MongoDB ID"""
        try:
            result = self.collection.find_one({'_id': ObjectId(id)})
            if result:
                result['_id'] = str(result['_id'])
            return result
        except Exception as e:
            return None

    def get_by_username_and_repo(self, username: str, repo_full_name: str) -> Optional[Dict]:
        """Get contributor by username and repository"""
        result = self.collection.find_one({
            'username': username,
            'repository': repo_full_name
        })
        if result:
            result['_id'] = str(result['_id'])
        return result

    def get_all(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all contributors with optional filters"""
        query = filters or {}
        results = list(self.collection.find(query))
        for result in results:
            result['_id'] = str(result['_id'])
        return results

    def get_by_repository(self, repo_full_name: str) -> List[Dict]:
        """Get all contributors for a specific repository"""
        return self.get_all({'repository': repo_full_name})

    def create(self, data: Dict) -> Dict:
        """Create a new contributor record"""
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    def update(self, id: str, data: Dict) -> bool:
        """Update contributor data"""
        try:
            data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': data}
            )
            return result.modified_count > 0
        except Exception as e:
            return False

    def upsert_contributor(self, username: str, repo_full_name: str, data: Dict) -> Dict:
        """Create or update contributor"""
        existing = self.get_by_username_and_repo(username, repo_full_name)

        if existing:
            self.update(existing['_id'], data)
            return {**existing, **data}
        else:
            data['username'] = username
            data['repository'] = repo_full_name
            return self.create(data)

    def delete(self, id: str) -> bool:
        """Delete a contributor"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(id)})
            return result.deleted_count > 0
        except Exception as e:
            return False

    def bulk_upsert(self, contributors: List[Dict]) -> int:
        """Bulk upsert multiple contributors"""
        count = 0
        for contributor in contributors:
            try:
                self.upsert_contributor(
                    username=contributor['username'],
                    repo_full_name=contributor['repository'],
                    data=contributor
                )
                count += 1
            except Exception as e:
                continue
        return count


# core/repositories/repo_repository.py
from typing import Dict, List, Optional
from bson import ObjectId
from datetime import datetime
from .base_repository import BaseRepository


class RepositoryRepository(BaseRepository):
    """
    Repository Repository - Manages GitHub repository data in MongoDB
    """

    def __init__(self):
        super().__init__('repositories')

    def get_by_id(self, id: str) -> Optional[Dict]:
        """Get repository by MongoDB ID"""
        try:
            result = self.collection.find_one({'_id': ObjectId(id)})
            if result:
                result['_id'] = str(result['_id'])
            return result
        except Exception as e:
            return None

    def get_by_full_name(self, full_name: str) -> Optional[Dict]:
        """Get repository by full name (owner/repo)"""
        result = self.collection.find_one({'full_name': full_name})
        if result:
            result['_id'] = str(result['_id'])
        return result

    def get_all(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all repositories with optional filters"""
        query = filters or {}
        results = list(self.collection.find(query))
        for result in results:
            result['_id'] = str(result['_id'])
        return results

    def get_by_owner(self, owner: str) -> List[Dict]:
        """Get all repositories by owner"""
        return self.get_all({'owner': owner})

    def create(self, data: Dict) -> Dict:
        """Create a new repository record"""
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    def update(self, id: str, data: Dict) -> bool:
        """Update repository data"""
        try:
            data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': data}
            )
            return result.modified_count > 0
        except Exception as e:
            return False

    def upsert_repository(self, full_name: str, data: Dict) -> Dict:
        """Create or update repository"""
        existing = self.get_by_full_name(full_name)

        if existing:
            self.update(existing['_id'], data)
            return {**existing, **data}
        else:
            data['full_name'] = full_name
            return self.create(data)

    def delete(self, id: str) -> bool:
        """Delete a repository"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(id)})
            return result.deleted_count > 0
        except Exception as e:
            return False