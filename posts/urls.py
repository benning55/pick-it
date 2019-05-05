from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:car_id>/', views.detail, name='detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/rent/<int:car_id>/', views.rent_post, name='rent_post'),
    path('post/rent/decide/<int:rent_id>/', views.rent_decide, name='rent_decide'),
    path('post/rent/accept/<int:rent_id>/', views.rent_accept, name='rent_accept'),
    path('post/rent/decline/<int:rent_id>/', views.rent_decline, name='rent_decline'),
    path('post/delete/<int:car_id>/', views.delete, name='delete'),
    path('post/update/<int:car_id>/', views.update, name='update'),
    path('post/report/<int:car_id>/', views.report, name='report')
]
