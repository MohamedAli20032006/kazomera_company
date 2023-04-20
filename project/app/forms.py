from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

class UserRegistrationForm(UserCreationForm):
    is_investor = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_investor', ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['action']
