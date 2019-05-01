from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Car


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'posts/home.html', context=context)


class PostListView(ListView):
    model = Car
    template_name = 'posts/home.html'
    context_object_name = 'cars'


class PostDetailView(DetailView):
    model = Car
    template_name = 'posts/detail.html'


class PostCreateView(CreateView):
    model = Car
    template_name = 'posts/new_post.html'
    fields = '__all__'


def about(request):
    return render(request, 'posts/about.html')
