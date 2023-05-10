from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import Publication, Project, SavedItem, News, Notification
from .serializers import *

from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here

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

class SavedItemList(generics.ListCreateAPIView):
    queryset = SavedItem.objects.all()
    serializer_class = SavedItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavedItemDetail(generics.RetrieveDestroyAPIView):
    queryset = SavedItem.objects.all()
    serializer_class = SavedItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)

class NotificationDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)