from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = '/login/intro1'  # 로그인 성공 후 이동 경로
        return path