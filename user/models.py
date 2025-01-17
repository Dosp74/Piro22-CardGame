from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)  # 유저 이름
    point = models.IntegerField(default=0)  # 유저 점수

    # groups와 user_permissions 필드에 대해 related_name 설정 추가
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # related_name을 'custom_user_groups'로 설정
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # related_name을 'custom_user_permissions'로 설정
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.point} points)"