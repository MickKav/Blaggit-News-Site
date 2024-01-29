from django.urls import path
from . import views
from news.views import PostList as home

app_name = 'contact'

urlpatterns = [
    path('contact/', views.ContactMessage.as_view(), name='contact'),
    path('', views.home, name='home'),
]
