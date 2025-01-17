from django.urls import path
from ranking import views

app_name = 'ranking'

urlpatterns = [
    path('', views.ranking, name='ranking'),
]