# user/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)  # 유저 이름
    point = models.IntegerField(default=0)  # 유저 점수

    def __str__(self):
        return f"{self.username} ({self.point} points)"
