from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from .models import User

class UserAdmin(BaseUserAdmin):
    # 사용자 정의 필드를 표시
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('point',)}),  # 추가 필드
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'point', 'is_staff')  # 목록에서 표시할 필드

admin.site.register(User, UserAdmin)