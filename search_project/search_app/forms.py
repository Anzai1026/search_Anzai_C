from django import forms
from .models import Product
from django.contrib.auth.forms import AuthenticationForm
class SearchForm(forms.Form):
    query = forms.CharField(
        label='検索キーワード',
        max_length=100,  # CharField で max_length が有効です
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))