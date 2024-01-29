from django.urls import path, include
from . import views
from .views import AddCategory, PostEdit, AddPost, PostDetail

app_name = 'news'

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('edit/<slug:slug>/', PostEdit.as_view(), name='post_edit'),
    path('vote/<slug:slug>/', views.PostVote.as_view(), name='post_vote'),
    path('delete/<slug:slug>/', views.PostDelete.as_view(), name='post_delete'),
    path('add/', AddPost.as_view(), name='post_add'),
    path('addcategory/', AddCategory.as_view(), name='add_category'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
