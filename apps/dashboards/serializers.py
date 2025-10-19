# apps/dashboards/serializers.py
from rest_framework import serializers


class MetricsSerializer(serializers.Serializer):
    commits = serializers.DictField()
    issues = serializers.DictField()
    pull_requests = serializers.DictField()


class ChartsSerializer(serializers.Serializer):
    commits_timeline = serializers.ListField()
    code_changes = serializers.ListField()
    issues_status = serializers.ListField()
    prs_status = serializers.ListField()


class DashboardSerializer(serializers.Serializer):
    username = serializers.CharField()
    repository = serializers.CharField()
    generated_at = serializers.DateTimeField()
    metrics = MetricsSerializer()
    charts = ChartsSerializer()
    recent_activity = serializers.ListField()
    summary = serializers.DictField()


class RepositorySerializer(serializers.Serializer):
    name = serializers.CharField()
    full_name = serializers.CharField()
    owner = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    url = serializers.URLField()
    stars = serializers.IntegerField()
    forks = serializers.IntegerField()
    language = serializers.CharField(allow_null=True)


class ContributorSerializer(serializers.Serializer):
    username = serializers.CharField()
    avatar_url = serializers.URLField()
    profile_url = serializers.URLField()
    contributions = serializers.IntegerField()