from django.shortcuts import render, redirect
# from .models import Ranking이 아니라 accounts.models에 있는 count를 가져와야 한다!!
# from accounts.models import Account

def ranking(request):
    '''
    # 유저명
    accounts = Account.objects.all().order_by('-score')[:3]
    accounts = Account.objects.values('user_name', 'score').order_by('-score')[:3]

    context = {
        'accounts': accounts,
    }

    return render(request, 'ranking/ranking.html', context)
    '''
    return render(request, 'ranking/ranking.html')