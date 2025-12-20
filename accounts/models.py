from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Create your models here.
class ActiveUserProfileManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    profile_pic =models.CharField(max_length=1024, blank=True, null=True)

    objects = models.Manager()
    active = ActiveUserProfileManger()
    
    class Meta:
        db_table = 'user_profiles'  # correct way to set table name
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        
    def __str__(self):
        return self.user.username

class GithubAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="github_account")
    access_token = models.CharField(max_length=255)
    github_username = models.CharField(max_length=255, blank=True, null=True)
    linked_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    active = ActiveUserProfileManger()

    class Meta:
        db_table = "github_accounts"
        verbose_name = "Github Account"
        verbose_name_plural = "Github Accounts"

    def __str__(self):
        return f"{self.user.username}'s GitHub account"