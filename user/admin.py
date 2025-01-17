from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # 사용자 정의 필드를 표시
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('point',)}),  # 추가 필드
    )

admin.site.register(User, UserAdmin)