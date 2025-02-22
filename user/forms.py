from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# 회원가입 폼
class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2',]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update({'placeholder': '아이디를 입력하세요'})
    self.fields['password1'].widget.attrs.update({'placeholder': '비밀번호를 입력하세요'})
    self.fields['password2'].widget.attrs.update({'placeholder': '비밀번호 확인'})

class LoginForm(AuthenticationForm):
  username = forms.CharField(
    widget = forms.TextInput(attrs={'placeholder': '아이디를 입력하세요'})
  )
  password = forms.CharField(
    widget = forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력하세요'})
  )