from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm


def login(request):
    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now can login {username}!')
            return redirect('/accounts/login/')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
