from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
]