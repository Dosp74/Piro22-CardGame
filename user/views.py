import requests
from django.shortcuts import render, redirect
from django.conf import settings

def intro1_view(request):
    return render(request, 'login/intro1.html')

def intro2_view(request):
    return render(request, 'login/intro2.html')

def signup_view(request):
    return render(request, 'login/signup.html')

def login_view(request):
    return render(request, 'login/login.html')

def user_list(request):
    return render(request, 'main/list.html')

from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount

def kakao_callback(request):
    # 카카오 로그인 후 리디렉션된 URL에서 인증 코드 받기
    code = request.GET.get('code')
    client_id = settings.KAKAO_CLIENT_ID  # 카카오에서 발급받은 REST API 키
    redirect_uri = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'

    # 카카오로부터 액세스 토큰을 받는 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code': code,
    }
    
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')

    # 액세스 토큰을 사용하여 카카오 사용자 정보 요청
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    # 사용자 정보에서 nickname 추출
    nickname = user_info.get('properties', {}).get('nickname')

    # 추출한 nickname을 템플릿에 전달
    return render(request, 'login/intro2.html', {'nickname': nickname})


def kakao_login(request):
    # 카카오 로그인 URL 생성
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = 'http://127.0.0.1:8000/accounts/kakao/login/callback/'
    kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"

    # 카카오 로그인 페이지로 리디렉션
    return redirect(kakao_auth_url)
