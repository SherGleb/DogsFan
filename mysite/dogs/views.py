from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


# Create your views here.


class DogsHome(DataMixin, ListView):
    model = Dogs
    template_name = 'dogs/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    # Возвращаем только те записи из модели, которые опубликованы
    # Можно настроить опубликованность через админ панель
    # select_related - отложенный запрос, уменьшающий нагрузку на бд
    def get_queryset(self):
        return Dogs.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Dogs.objects.all()
#     cats = Category.objects.all()
#     context = {'title': 'Главная страница',
#                'cats': cats,
#                'posts': posts,
#                'menu': menu,
#                'cats_selected': 0,
#                }
#     return render(request, 'dogs/index.html', context=context)


def about(request):
    return render(request, 'dogs/about.html', {'title': 'О сайте', 'menu': menu})


# def adddog(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         # request.POST - данные от юзера, request.FILES - файлы (фото)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try except здесь уже не нужны, но мне лень
#             try:
#                 form.save() # Добавляем в бд введенные пользователем данные
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Post adding error')
#     else:
#         form = AddPostForm()
#     return render(request, 'dogs/adddog.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'dogs/adddog.html'
    # После добавления статьи будем перенаправлены на страницу home
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'dogs/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse('Авторизация')


# def show_post(request, post_slug):
#     post = get_object_or_404(Dogs, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'dogs/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Dogs
    template_name = 'dogs/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class DogsCategory(DataMixin, ListView):
    model = Dogs
    template_name = 'dogs/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Dogs.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Категория - " + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_slug):
#     cat_id = get_object_or_404(Category, slug=cat_slug)
#     posts = Dogs.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'dogs/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'dogs/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    # Функция для автоматического входа в аккаунт при
    # успешной регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'dogs/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
