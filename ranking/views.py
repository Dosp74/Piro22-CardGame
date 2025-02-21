from django.shortcuts import render
from user.models import User

def ranking(request):
    users = User.objects.all().order_by('-point')[:3]

    context = {
        'users': users,
    }

    return render(request, 'ranking/ranking.html', context)