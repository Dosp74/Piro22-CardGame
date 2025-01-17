from django.shortcuts import render

def signup_view(request):
    return render(request, 'login/signup.html')

def login_view(request):
    return render(request, 'login/login.html')

def user_list(request):
    return render(request, 'main/list.html')