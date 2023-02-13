from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.db.models import Q

import json
from django.views import View
from django.contrib.contenttypes.models import ContentType


from blog.forms import *
from blog.utils import DataMixin, header_menu, footer_menu


class BlogHome(DataMixin, ListView):
    model = Blog
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related('cat')

    # переобпределение контекста - добавление в него данных, которые отсутствуют в models.Blog
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        c_def = self.get_user_data()
        context.update(c_def)
        return context


class AddPost(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "blog/addpage.html"
    # После создания записи перенаправление в "home"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("login")

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = self.request.user
            new_post.save()
            return redirect("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить рецепт"
        c_def = self.get_user_data()
        context.update(c_def)
        return context


class PostUpdateView(DataMixin, UpdateView):
    model = Blog
    form_class = AddPostForm
    template_name = "blog/addpage.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        author = Blog.objects.get(slug=self.kwargs["slug"]).author
        if request.user.is_authenticated and request.user == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить рецепт"
        c_def = self.get_user_data()
        context.update(c_def)
        return context

class DeletePostView(DataMixin, DeleteView):
    model = Blog
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("home")
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        author = Blog.objects.get(slug=self.kwargs["slug"]).author
        if request.user.is_authenticated and request.user == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удалить рецепт"
        c_def = self.get_user_data()
        context.update(c_def)
        return context


class ShowPost(DataMixin, DetailView):
    model = Blog
    template_name = "blog/post.html"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_data()
        context.update(c_def)
        context["cat_selected"] = context["post"].cat_id
        context["title"] = context["post"]
        return context


class BlogCategory(DataMixin, ListView):
    model = Category
    template_name = "blog/index.html"
    context_object_name = "posts"
    allowe_epty = False

    # отображение только записей БД с полученным cat_slug + они должны быть опубликованы
    def get_queryset(self):
        return Blog.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True).select_related('cat')

    # переобпределение контекста - добавление в него данных, которые отсутствуют в models.Category
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_data()
        context.update(c_def)
        cat = Category.objects.get(slug=self.kwargs["cat_slug"])
        # если cat_selected с указанным cat_id, то в левом меню категория отображаения как выбранная
        context["cat_selected"] = cat.pk
        context["title"] = "категория: " + str(cat.name)
        return context


class SearchPost(DataMixin, ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            print(query, 1)
            search_posts = Blog.objects.filter((Q(title__icontains=query) | Q(content__icontains=query)) & Q(is_published=True)).select_related('cat')
            return search_posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_data(title="Поиск по сайту")
        context.update(c_def)
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "blog/register.html"
    success_url = "home"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_data()
        context.update(c_def)
        return context


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_data(title="Авторизация")
        context.update(c_def)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("home")

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_data(title="Обратная связь")
        context.update(c_def)
        if self.request.user.is_authenticated:
            context["form"].fields["name"].initial = self.request.user
            context["form"].fields["email"].initial = self.request.user.email
        return context


class VotesView(View):
    model = None  # Модель данных - черех маршрут в urls.py сюда будет передана модель
    vote_type = None  # аналогично с model будет передан LikeDislike.LIKE или LikeDislike.DISLIKE

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )


def logout_user(request):
    logout(request)
    return redirect("login")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def about(request):
    cats = Category.objects.all()
    return render(request, 'blog/about.html', {'title': 'О сайте',
                                               "header_menu": header_menu,
                                               "footer_menu": footer_menu,
                                               "cats": cats})

