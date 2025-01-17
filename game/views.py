import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from user.models import User  # User 모델 가져오기
from game.models import Game  # Game 모델 가져오기


def start_game(request):
    def generate_random_cards():
        # 1~10 중 5개의 랜덤한 숫자를 반환
        return random.sample(range(1, 11), 5)

    if request.method == "GET":
        # GET 요청 처리: 랜덤 카드와 사용자 목록 생성
        context = {
            "cards": generate_random_cards(),
            "users": User.objects.exclude(id=request.user.id),  # 현재 사용자 제외
        }
        return render(request, "game/start_game.html", context)

    elif request.method == "POST":
        # POST 요청 처리
        selected_card = request.POST.get("selected_card")  # `selected_card`에서 값 가져오기
        defender_id = request.POST.get("defender_id")

        if not selected_card or not defender_id:
            return HttpResponseBadRequest("Invalid input. Please select a card and an opponent.")

        # 데이터 타입 변환 및 유효성 검사
        try:
            attacker_card = int(selected_card)  # `selected_card`를 정수로 변환
        except ValueError:
            return HttpResponseBadRequest("Invalid card value.")

        defender = get_object_or_404(User, id=defender_id)

        # 새로운 게임 생성
        game = Game.objects.create(
            attacker=request.user,
            defender=defender,
            attacker_card=attacker_card
        )

        # 결과 페이지로 리다이렉트
        return redirect("game:list_view")

    # 잘못된 HTTP 메서드 처리
    return HttpResponseNotAllowed(["GET", "POST"])



@login_required
def game_detail(request, game_id):
    # 게임 정보 가져오기
    game = get_object_or_404(Game, id=game_id)
    
    # 로그인한 사용자의 관점에서 게임 상태 확인
    if game.result == "":
        if request.user == game.attacker:
            status = "waiting"  # 진행 중 (4-1 상황)
        elif request.user == game.defender:
            status = "counterattack"  # 반격 가능 (4-2 상황)
    else:
        status = "finished"  # 종료 (4-3 상황)

    # 사용자의 게임 결과 가져오기
    user_result = game.get_result_for_user(request.user) if game.result else None

    # 컨텍스트에 데이터 추가
    context = {
        "game": game,
        "status": status,
        "user_result": user_result,  # 사용자의 게임 결과
    }

    return render(request, "game/game_detail.html", context)

@login_required
def cancel_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 게임을 취소할 수 있는 상태인지 확인
    if request.user == game.attacker and game.defender_card is None:
        game.delete()
        return redirect('game:list_view')  # 게임 목록 페이지 구현 필요
    else:
        return redirect('game:game_detail', game_id=game_id) # templates/game/game_detail.html로 리다이렉트

@login_required
def counterattack(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == "GET":  # 반격 페이지 표시
        print(f"GET Request: User={request.user}, Game Defender={game.defender}, Defender Card={game.defender_card}")

        if request.user != game.defender or game.defender_card is not None:
            print("Redirecting to game detail: Unauthorized access or card already set.")
            return redirect('game:game_detail', game_id=game_id)

        # 5장의 랜덤 카드 생성
        cards = random.sample(range(1, 11), 5)
        return render(request, "game/counterattack.html", {
            "game": game,
            "cards": cards,
        })

    elif request.method == "POST":  # 폼 제출 처리
        print(f"POST Request: User={request.user}, Game Defender={game.defender}, Defender Card={game.defender_card}")

        if request.user != game.defender or game.defender_card is not None:
            print("Redirecting to game detail: Unauthorized access or card already set.")
            return redirect('game:game_detail', game_id=game_id)

        selected_card = request.POST.get('selected_card')
        print(f"Selected card: {selected_card}")

        if not selected_card:
            print("No card selected. Redirecting to counterattack page.")
            return redirect('game:counterattack', game_id=game_id)

        try:
            game.defender_card = int(selected_card)
        except ValueError:
            print(f"Invalid card value: {selected_card}. Redirecting to counterattack page.")
            return redirect('game:counterattack', game_id=game_id)

        # 승리 조건 설정
        if not game.winning_condition:
            game.winning_condition = random.choice([choice[0] for choice in Game.WINNING_CONDITIONS])

        game.save()
        game.determine_result()  # 게임 결과 결정

        print(f"Game updated: {game}")
        return redirect('game:game_detail', game_id=game_id)

    print("Invalid HTTP method. Only GET and POST are allowed.")
    return redirect('game:game_detail', game_id=game_id)
    
def update_point(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if game.result == "ATTACKER_WIN":
        game.attacker.point += game.attacker_card
        game.defender.point -= game.attacker_card
    elif game.result == "DEFENDER_WIN":
        game.defender.point += game.defender_card
        game.attacker.point -= game.defender_card
    game.attacker.save()
    game.defender.save()
    
    return redirect('game:game_detail', game_id=game_id)

from django.shortcuts import render
from .models import Game

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Game

@login_required
def list_view(request):
    user = request.user  # 현재 로그인한 사용자

    # 사용자가 참여한 모든 게임 가져오기
    games_as_attacker = Game.objects.filter(attacker=user)
    games_as_defender = Game.objects.filter(defender=user)
    all_games = games_as_attacker | games_as_defender

    # 게임과 상태를 저장
    games_with_status = []
    for game in all_games:
        if game.result == "":  # 결과가 없는 경우
            if user == game.attacker and not game.defender_card:
                status = "waiting"  # 방어자가 아직 응답하지 않은 상태
            elif user == game.defender and not game.defender_card:
                status = "counterattack"  # 방어자가 반격해야 하는 상태
        else:
            status = "finished"  # 게임이 종료된 상태

        user_result = game.get_result_for_user(user)
        games_with_status.append({
            "game": game,
            "status": status,
            "user_result": user_result
        })

    # 템플릿 렌더링
    context = {
        "user": user,
        "games_with_status": games_with_status,
    }
    return render(request, "game/list.html", context)
