from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('post/new/', views.create_post, name='create_post')
]
