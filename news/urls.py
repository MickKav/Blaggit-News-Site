from django.urls import path, include
from . import views
from .views import AddCategory, CategoryView, ArticleList, ArticleDetail, PostEdit, AddPost

app_name = 'news'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('edit/<slug:slug>/', PostEdit, name='post_edit'),
    path('vote/<slug:slug>', views.PostVote.as_view(), name='post_vote'),
    path('delete/<slug:slug>', views.PostDelete.as_view(), name='post_delete'),
    path('add/', AddPost, name='post_add'),
    path('addcategory/', AddCategory, name='add_category'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('article/<slug:slug>/', ArticleDetail.as_view(), name='article_detail'),
    path('category/<str:cats>/', CategoryView, name='category'),
]