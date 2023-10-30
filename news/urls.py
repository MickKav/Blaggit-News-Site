from django.urls import path, include
from . import views
from .views import AuthorProfileView, AddCategory, CategoryView

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('edit/<slug:slug>/', views.PostEdit.as_view(), name='post_edit'),
    path('vote/<slug:slug>', views.PostVote.as_view(), name='post_vote'),
    path('delete/<slug:slug>', views.PostDelete.as_view(), name='post_delete'),
    path('post_add/', views.AddPost.as_view(), name='post_add'),
    path('post_category/', views.AddCategory.as_view(), name='post_category'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('author/profile/', AuthorProfileView.as_view(), name='author_profile'),
    path('category/<str:cats>/', CategoryView, name='category'),
]