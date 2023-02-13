from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from blog.models import Blog, LikeDislike
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', BlogHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPost.as_view(), name='add_page'),
    path('post/<slug:slug>/edite/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', DeletePostView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'),
    re_path('search/', SearchPost.as_view(), name='search'),
    path('api/blog/<int:pk>/like/', login_required(VotesView.as_view(model=Blog, vote_type=LikeDislike.LIKE)), name='post_like'),
    path('api/blog/<int:pk>/dislike/', login_required(VotesView.as_view(model=Blog, vote_type=LikeDislike.DISLIKE)), name='post_dislike'),
]
