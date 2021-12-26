from django import forms
from .models import Post
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title', 'content', 'category')

  # 定型文
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = {'username', 'email', 'password1', 'password2'}
    # for field in fields:
    #   field.widget.attrs['class'] = 'form-control'
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'