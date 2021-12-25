from django.shortcuts import render, resolve_url
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

class Index(TemplateView):
  template_name = 'myapp/index.html'
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      post_list = Post.objects.all().order_by('-created_at')
      context = {
        'post_list': post_list,
      }
      return context

class PostCreate(CreateView):
  model = Post
  form_class = PostForm
  success_url = reverse_lazy('myapp:index')

class PostDetail(DetailView):
  model = Post

class PostUpdate(UpdateView):
  model = Post
  form_class = PostForm
  def get_success_url(self):
    messages.info(self.request, 'Postを更新しました')
    return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])

class PostDelete(DeleteView):
  model = Post
  def get_success_url(self):
    messages.info(self.request, 'Postを削除しました')
    return resolve_url('myapp:index')

class PostList(ListView):
  model = Post
  def get_queryset(self):
    return Post.objects.all().order_by('-created_at')

class Login(LoginView):
  form_class = LoginForm
  template_name = 'myapp/login.html'
  def get_success_url(self):
    messages.info(self.request, 'Sign Inしました')
    return resolve_url('myapp:index')

class Logout(LogoutView):
  template_name = 'myapp/logout.html'
  # def get_success_url(self):
  #   messages.info(self.request, 'Sign Outしました')
  #   return resolve_url('myapp:index')