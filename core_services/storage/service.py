from django.conf import settings
from .storage_buckets import LocalStorage, MinioStorage

class StorageService:
    """Unified global storage service that supports local + MinIO."""

    _instance=None #singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_backends()

        return cls._instance


    def _init_backends(self):
        self.local=LocalStorage()
        self.minio=MinioStorage()
        self.default_backend = (
            self.minio if settings.DEFAULT_STORAGE == 'minio' else self.local
        )

    def upload(self, path, file_obj):
        """Upload file to the default backend."""
        return self.default_backend.save(path, file_obj)

    def url(self, path, temp=True, expire_seconds=3600):
        """Return public URL for file from default backend."""
        if isinstance(self.default_backend, MinioStorage) and temp:
            return self.default_backend.get_url(path, expire_seconds)
        return self.default_backend.url(path)

    def backend(self, name):
        """Access a specific backend by name ('local' or 'minio')."""
        if name == 'local':
            return self.local
        elif name == 'minio':
            return self.minio
        raise ValueError(f"Unknown storage backend {name}")

storage_service = StorageService()