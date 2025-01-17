from django.urls import path
from user import views

app_name='user'

urlpatterns = [
    path('', views.intro1_view, name='intro1'),
    path('intro2/', views.intro2_view, name='intro2'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('list',views.user_list,name = 'user_list'),
]
