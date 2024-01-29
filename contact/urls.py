from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('contact/', views.ContactMessage.as_view(), name='contact'),
]