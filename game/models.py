from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import random

class Game(models.Model):
    WINNING_CONDITIONS = [
        ("HIGH", "Higher number wins"),
        ("LOW", "Lower number wins")
    ]

    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 사용자 정의 User 모델을 참조
        related_name="games_attacked",
        on_delete=models.CASCADE
    )
    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 사용자 정의 User 모델을 참조
        related_name="games_defended",
        on_delete=models.CASCADE
    )
    attacker_card = models.PositiveIntegerField(null=True, blank=True)  # 공격자가 선택한 카드
    defender_card = models.PositiveIntegerField(null=True, blank=True)  # 방어자가 선택한 카드
    winning_condition = models.CharField(max_length=10, choices=WINNING_CONDITIONS, default="HIGH")  # 승리 조건
    result = models.CharField(max_length=10, blank=True)  

    def determine_result(self):
        """게임의 승패를 결정하는 로직"""
        if self.attacker_card is not None and self.defender_card is not None:
            if self.attacker_card == self.defender_card:
                self.result = "DRAW"
            elif (self.winning_condition == "HIGH" and self.attacker_card > self.defender_card) or \
                 (self.winning_condition == "LOW" and self.attacker_card < self.defender_card):
                self.result = "ATTACKER_WIN"
            else:
                self.result = "DEFENDER_WIN"
            self.save()

    def get_result_for_user(self, user):
        """
        로그인한 사용자의 관점에서 게임 결과를 반환합니다.
        - WIN: 해당 유저가 승리한 경우
        - LOSE: 해당 유저가 패배한 경우
        - DRAW: 무승부
        """
        if user == self.attacker:
            if self.result == "ATTACKER_WIN":
                return "WIN"
            elif self.result == "DEFENDER_WIN":
                return "LOSE"
            elif self.result == "DRAW":
                return "DRAW"
        elif user == self.defender:
            if self.result == "DEFENDER_WIN":
                return "WIN"
            elif self.result == "ATTACKER_WIN":
                return "LOSE"
            elif self.result == "DRAW":
                return "DRAW"
        return "NOT_PARTICIPATING"