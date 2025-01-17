from django.urls import path
from user import views

app_name='user'

urlpatterns = [
    path('signup', views.signup_view, name='signup'), 
    path('', views.login_view, name='login'),
    path('list',views.user_list,name = 'user_list')
]
