from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from gramm.models import *


def index(request):
    posts = Post.objects.order_by('-id').all()
    return render(request, 'gramm/index.html', {'posts': posts})


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = RegistrationForm()
    return render(request, 'gramm/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'gramm/login.html', {'msg': 'login or password is not correct'})
    return render(request, 'gramm/login.html')


@login_required
def profile_user(request):
    active_user = Person.objects.filter(user=request.user).first()
    posts = Post.objects.filter(user=active_user.user).order_by('-id').all()
    return render(request, 'gramm/profile.html', {'user': active_user, 'posts': posts})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'gramm/addpost.html', {'form': form})
    form = PostForm(user=request.user)
    return render(request, 'gramm/addpost.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')
