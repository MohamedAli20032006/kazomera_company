from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *

from django.contrib.auth.models import User
from rest_framework import generics
from .models import Publication, Project
from .serializers import UserSerializer, PublicationSerializer, ProjectSerializer


@login_required
def user_page(request):
    user = request.user
    publications = Publication.objects.filter(author=user)
    context = {
        'user': user,
        'publications': publications
    }
    return render(request, 'user_page.html', context)


def news_page(request):
    publications = Publication.objects.all().order_by('-created_at')
    context = {
        'publications': publications
    }
    return render(request, 'news_page.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-id')
    form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

@login_required
def projects_page(request):
    projects = Project.objects.all().order_by('-created_at')
    context = {
        'projects': projects
    }
    return render(request, 'projects_page.html', context)


@login_required
def contributions_page(request):
    user = request.user
    contributions = Contribution.objects.filter(contributor=user)
    context = {
        'contributions': contributions
    }
    return render(request, 'contributions_page.html', context)


@login_required
def investments_page(request):
    user = request.user
    investments = Investment.objects.filter(investor=user)
    context = {
        'investments': investments
    }
    return render(request, 'investments_page.html', context)


@login_required
def saved_items_page(request):
    user = request.user
    saved_projects = user.saved_projects.all()
    saved_publications = user.saved_publications.all()
    context = {
        'saved_projects': saved_projects,
        'saved_publications': saved_publications
    }
    return render(request, 'saved_items_page.html', context)




class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PublicationList(generics.ListAPIView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

