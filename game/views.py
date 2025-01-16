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

@login_required
def cancel_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 게임을 취소할 수 있는 상태인지 확인
    if request.user == game.attacker and game.defender_card is None:
        game.delete()
        return redirect('game_list')  # 게임 목록 페이지 구현 필요
    else:
        return redirect('game:game_detail', game_id=game_id) # templates/game/game_detail.html로 리다이렉트

@login_required
def counterattack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == "GET": # 반격하는 페이지 표시
        if request.user != game.defender or game.defender_card is not None:
            return redirect('game:game_detail', game_id=game_id)
        
        # 5장의 랜덤 카드 생성
        cards = random.sample(range(1, 11), 5)
        return render(request, "game/counterattack.html", {
            "game": game,
            "cards": cards,
        })
    
    elif request.method == "POST": # 폼 제출 시
        if request.user != game.defender or game.defender_card is not None:
            return redirect('game:game_detail', game_id=game_id)
        
        selected_card = int(request.POST.get('selected_card'))
        
        # 선택한 카드 저장
        game.defender_card = selected_card
        
        # 승리 조건이 설정되어 있지 않다면 랜덤으로 설정
        if not game.winning_condition:
            game.winning_condition = random.choice([choice[0] for choice in Game.WINNING_CONDITIONS])
        
        game.save()
        game.determine_result()  # 게임 결과 결정
        
        return redirect('game:game_detail', game_id=game_id)