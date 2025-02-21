import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse  # reverse 함수 가져오기
from .utils import get_kakao_access_token, get_kakao_user_info  # utils에서 함수 가져오기
from user.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout

User = get_user_model()

def intro1_view(request):
    return render(request, 'login/intro1.html')

def intro2_view(request):
    # 현재 로그인된 사용자의 username 가져오기
    if request.user.is_authenticated:
        username = request.user.username  # 현재 로그인된 사용자의 username
    else:
        username = None  # 로그인되지 않은 경우

    context = {
        'username': username
    }

    return render(request, 'login/intro2.html', context)

def signup_view(request):
    return render(request, 'login/signup.html')

def login_view(request):
    return render(request, 'login/login.html')

def user_list(request):
    return render(request, 'main/list.html')

def kakao_callback(request):
    """카카오 로그인 콜백 처리"""
    # 1. 인증 코드 가져오기
    code = request.GET.get('code')
    if not code:
        return render(request, 'error.html', {'message': 'Authorization code not provided.'})

    # 2. Access Token 요청
    access_token = get_kakao_access_token(code)
    if not access_token:
        return render(request, 'error.html', {'message': 'Failed to get access token.'})

    # 3. 사용자 정보 요청
    user_info = get_kakao_user_info(access_token)
    if not user_info:
        return render(request, 'error.html', {'message': 'Failed to get user info.'})

    # 4. 사용자 정보에서 ID, 닉네임, 프로필 사진 추출
    kakao_id = user_info.get('id')
    nickname = user_info.get('properties', {}).get('nickname', 'Unknown')
    profile_image = user_info.get('properties', {}).get('profile_image', None)

    # 5. 사용자 계정 생성 또는 업데이트
    user, created = User.objects.get_or_create(username=nickname)
    user.first_name = nickname
    user.profile_image = profile_image
    if created:
        user.first_name = nickname
        user.profile_image = profile_image
        user.save()
    else:
        user.save()

    user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
    login(request, user)

    # 6. 성공 시 리디렉트
    return redirect(reverse('user:intro2'))

def kakao_login(request):
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = settings.KAKAO_REDIRECT_URI
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&prompt=login"
    return redirect(kakao_auth_url)

def kakao_logout(access_token):
    logout_url = "https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(logout_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to logout: {response.json()}")
        return None

def user_logout(request):
    # 1. Django에서 사용자 로그아웃
    logout(request)

    # 2. 카카오 로그아웃 API 호출 (옵션)
    access_token = request.session.get('kakao_access_token')
    if access_token:
        kakao_logout(access_token)
        request.session.pop('kakao_access_token', None)

    # 3. 홈 또는 로그인 페이지로 리디렉트
    return redirect(reverse('user:login'))