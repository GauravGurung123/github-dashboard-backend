# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api/', include('apps.dashboards.urls')),
    path('repositories', RedirectView.as_view(url=f'{settings.FRONTEND_URL.rstrip("/")}/repositories', permanent=False)),
    path('repositories/', RedirectView.as_view(url=f'{settings.FRONTEND_URL.rstrip("/")}/repositories', permanent=False)),
    path('', RedirectView.as_view(url=settings.FRONTEND_URL, permanent=False)),
]

# Only serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# core/exceptions.py
class GitHubAPIException(Exception):
    """Custom exception for GitHub API errors"""
    pass


class RepositoryNotFoundException(Exception):
    """Repository not found exception"""
    pass


class ContributorNotFoundException(Exception):
    """Contributor not found exception"""
    pass