from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        print("CustomSocialAccountAdapter is called")  # 어댑터 실행 여부 확인
        print("Extra data from Kakao:", sociallogin.account.extra_data)  # 반환 데이터 출력
        return super().save_user(request, sociallogin, form)