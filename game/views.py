import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Game
from account.models import Account

def start_game(request):
    def generate_random_cards():
        #1~10 중 5개의 랜덤한 숫자를 반환
        return random.sample(range(1, 11), 5)

    if request.method == "GET":
        # 5장의 랜덤 카드를 생성
        cards = generate_random_cards() #5개의 카드 리스트
        users = Account.objects.exclude(id=request.user.id)  # 상대 유저 리스트
        return render(request, "game/start_game.html", {"cards": cards, "users": users})