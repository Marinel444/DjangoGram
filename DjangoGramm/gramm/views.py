from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from gramm.models import *


def index(request):
    posts = Post.objects.order_by('-id').all()
    like = []
    for post in posts:
        if Like.objects.filter(post=post).exists():
            like.append(Like.objects.filter(post=post).count())
        else:
            like.append(0)
    if request.method == 'POST':
        action = request.POST.get('action')
        post_like = Post.objects.filter(pk=action).first()
        if not Like.objects.filter(person_id=request.user,post=post_like).exists():
            new_like = Like.objects.create(person_id=request.user, post=post_like)
            new_like.save()

    data = zip(posts, like)
    context = [{'post': post, 'like_count': like_count} for post, like_count in data]
    return render(request, 'gramm/index.html', {'context': context})


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
def account_user(request, user_id):
    profile = Person.objects.filter(user_id=user_id).first()
    following = Follower.objects.filter(follower_id=profile.user, following_user_id=request.user).exists()
    data = {
        'user': profile,
        'following': following
    }
    if profile.user_id == request.user.id:
        return redirect('/profile/')

    if Post.objects.filter(user_id=profile.user_id).exists():
        posts = Post.objects.filter(user_id=profile.user_id).all()
        data['posts'] = posts

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'subscribe':
            subscribe = Follower.objects.create(follower_id=profile.user, following_user_id=request.user)
            subscribe.save()
            return redirect(request.path)
        if action == 'unsubscribe':
            unsubscribe = Follower.objects.filter(follower_id=profile.user, following_user_id=request.user).first()
            unsubscribe.delete()
            return redirect(request.path)

    return render(request, 'gramm/account.html', data)


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
