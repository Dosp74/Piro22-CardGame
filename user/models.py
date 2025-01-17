# user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)  # 유저 이름
    point = models.IntegerField(default=0)  # 유저 점수

    def __str__(self):
        return f"{self.username} ({self.point} points)"

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True, null=True)  # 닉네임
    profile_image = models.URLField(blank=True, null=True)  # 프로필 사진 (추가 가능)