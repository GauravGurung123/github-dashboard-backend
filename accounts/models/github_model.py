from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.utils import timezone


# Create your models here.
class ActiveManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class GithubAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="github_accounts")
    access_token = models.CharField(max_length=255)
    github_username = models.CharField(max_length=255, blank=True, null=True)
    linked_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # objects = models.manager
    # active = ActiveManger()
    # Managers
    objects = ActiveManger()  # default manager now filters deleted_at
    all_objects = models.Manager()  # access everything, Includes deleted

    class Meta:
        db_table = "github_accounts"
        verbose_name = "Github Account"
        verbose_name_plural = "Github Accounts"

    def __str__(self):
        return f"{self.user.username}'s GitHub account"

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()