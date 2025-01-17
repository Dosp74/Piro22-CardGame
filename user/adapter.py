from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # 기본 사용자 생성 로직
        user = super().save_user(request, sociallogin, form)

        # 카카오에서 받은 추가 데이터
        extra_data = sociallogin.account.extra_data
        nickname = extra_data.get('nickname')  # 닉네임 데이터
        profile_image = extra_data.get('profile_image')  # 프로필 사진 데이터 (필요시)

        # 사용자 모델에 저장
        user.username = nickname  # 닉네임 저장
        user.profile_image = profile_image  # 프로필 사진 저장 (CustomUser 모델에 추가한 경우)
        user.save()
        return user