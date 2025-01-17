import requests
from django.conf import settings  # settings를 가져옵니다.

def get_kakao_access_token(code):
    """카카오로부터 Access Token을 요청하는 함수"""
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.KAKAO_CLIENT_ID,  # settings에서 가져옴
        'client_secret': settings.KAKAO_CLIENT_SECRET,  # Client Secret 추가
        'redirect_uri': settings.KAKAO_REDIRECT_URI,  # Redirect URI
        'code': code,
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Failed to get access token: {response.json()}")
        return None

def get_kakao_user_info(access_token):
    """카카오로부터 사용자 정보를 요청하는 함수"""
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(user_info_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get user info: {response.json()}")
        return None