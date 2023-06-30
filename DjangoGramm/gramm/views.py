from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from gramm.models import *


def index(request):
    posts = Post.objects.all()
    return render(request, 'gramm/index.html', {'posts': posts})


def register_user(request):
    if request.method == 'POST':
        if request.POST.get('password1') != request.POST.get('password2') or len(request.POST.get('password1')) < 4:
            return render(request, 'gramm/register.html', {'error_message': 'password does not match'})
        if User.objects.filter(username=request.POST.get('username')).exists():
            return HttpResponse('<h3>This user already exists</h3>', status=200)
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            password=request.POST.get('password1'),
            is_active=True,
        )
        Person(
            user=user,
            bio=request.POST.get('bio'),
            photo=request.FILES.get('photo'),
        ).save()
        return redirect('/')
    return render(request, 'gramm/register.html')


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


def profile_user(request):
    active_user = Person.objects.filter(user=request.user).first()
    posts = Post.objects.filter(user=active_user.user).all()
    print(posts)
    return render(request, 'gramm/profile.html', {'user': active_user, 'posts': posts})


def add_post(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        comments = request.POST.get('comments')
        if photo is None:
            return render(request, 'gramm/addpost.html', {'msg': 'Photo not added'})
        Post(
            user=request.user,
            photo=photo,
            description=comments,
        ).save()
    return render(request, 'gramm/addpost.html')


def logout_user(request):
    logout(request)
    return redirect('/')
