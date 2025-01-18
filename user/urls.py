from django.urls import path
from user import views

app_name='user'

urlpatterns = [
    path('', views.intro1_view, name='intro1'),
    path('intro2/', views.intro2_view, name='intro2'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('list',views.user_list,name = 'user_list'),
    path('accounts/kakao/login/', views.kakao_login, name='kakao_login'),  # 카카오 로그인 요청
    path('accounts/kakao/login/callback/', views.kakao_callback, name='kakao_callback'),  # 카카오 리디렉션 후 처리
]