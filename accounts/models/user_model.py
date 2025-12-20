from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

from accounts.models import GithubAccount


# Create your models here.
class ActiveManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    active = ActiveManger()

    class Meta:
        db_table = 'user_profiles'  # correct way to set table name
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username

    @property
    def active_github_accounts(self):
        return self.user.github_accounts.filter(deleted_at__isnull=True)
        # return GithubAccount.objects.filter(user=self).first()
    @property
    def first_active_github_account(self):
        return self.active_github_accounts.first()
