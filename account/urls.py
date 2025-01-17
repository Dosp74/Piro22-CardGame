from django.urls import path
from account import views

app_name='account'

urlpatterns = [
    path('signup', views.signup_view, name='signup'), 
    path('', views.login_view, name='login'),
    path('list',views.user_list,name = 'user_list')
]
