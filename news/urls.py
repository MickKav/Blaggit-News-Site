from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('vote/<slug:slug>', views.PostVote.as_view(), name='post_vote'),
    path('delete/<slug:slug>', views.PostDelete.as_view(), name='post_delete'),
]