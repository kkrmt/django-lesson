from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post, Like, Category
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm, SearchForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# 自分のPostかどうか
class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        return post.author == self.request.user


class Index(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list,
        }
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Postを正常に投稿しました')
        return resolve_url('myapp:index')


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        detail_data = Post.objects.get(id=self.kwargs['pk'])
        category_posts = Post.objects.filter(category=detail_data.category).order_by('-created_at')[:5]
        context = {
            'object': detail_data,
            'category_posts': category_posts,
        }
        return context


class PostUpdate(OnlyMyPostMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request, 'Postを更新しました')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])


class PostDelete(OnlyMyPostMixin, DeleteView):
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


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'Sign Upしました')
        # todo: ??
        return HttpResponseRedirect(self.get_success_url())


@login_required
def like_add(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    is_liked = Like.objects.filter(post=post, user=user).count() > 0

    if is_liked:
        messages.warning(request, '既にお気に入り登録されています')
        return redirect('myapp:post_detail', post.id)

    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    messages.success(request, 'お気に入り登録しました')
    return redirect('myapp:post_detail', post.id)


class CategoryList(ListView):
    model = Category

    def get_queryset(self):
        return Category.objects.all().order_by('id')


class CategoryDetail(DetailView):
    model = Category
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        detail_data = Category.objects.get(name_en=self.kwargs['name_en'])
        category_posts = Post.objects.filter(category=detail_data.id).order_by('-created_at')
        params = {
            'object': detail_data,
            'category_posts': category_posts,
        }
        return params


def search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_word = search_form.cleaned_data['search_word']
            # OR検索
            search_list = Post.objects.filter(Q(title__icontains=search_word) | Q(content__icontains=search_word))

        params = {
            'search_word': search_word,
            'search_list': search_list,
        }
        return render(request, 'myapp/search.html', params)
