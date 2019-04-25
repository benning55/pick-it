from django.contrib import admin
from django.urls import path, include
from posts import views as post_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', post_view.home, name='home')
]
