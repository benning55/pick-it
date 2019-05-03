from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:car_id>/', views.detail, name='detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/rent/<int:car_id>/', views.rent_post, name='rent_post')
]
