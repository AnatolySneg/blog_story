from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Post


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
