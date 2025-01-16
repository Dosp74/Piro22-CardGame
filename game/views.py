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

@login_required
def game_detail(request, game_id):
    # 게임 정보 가져오기
    game = get_object_or_404(Game, id=game_id)
    
    # 로그인한 사용자의 관점에서 게임 상태 확인
    if game.result == "":
        if request.user == game.attacker:
            context = {"game": game, "status": "waiting"}  # 진행 중 (4-1 상황)
        elif request.user == game.defender:
            context = {"game": game, "status": "counterattack"}  # 반격 가능 (4-2 상황)
    else:
        context = {"game": game, "status": "finished"}  # 종료 (4-3 상황)

    return render(request, "game/game_detail.html", context)