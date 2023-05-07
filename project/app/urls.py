from django.contrib.auth.decorators import login_required

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    user_page,
    news_page,
    projects_page,
    contributions_page,
    investments_page,
    saved_items_page,
    SavedItemList,
    SavedItemDetail,
    NewsList,
    NewsDetail,
    NotificationList,
    NotificationDetail
)
from .views import UserList, PublicationList, ProjectList
from .views import post_detail, add_comment




urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='news_page'), name='logout'),
    path('user/', user_page, name='user_page'),
    path('news/', news_page, name='news_page'),
    path('projects/', projects_page, name='projects_page'),
    path('contributions/', contributions_page, name='contributions_page'),
    path('investments/', investments_page, name='investments_page'),
    path('saved-items/', saved_items_page, name='saved_items_page'),

    path('api/users/', UserList.as_view()),
    path('api/publications/', PublicationList.as_view()),
    path('api/projects/', ProjectList.as_view()),

    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),

    path('saved_items/', SavedItemList.as_view()),
    path('saved_items/<int:pk>/', SavedItemDetail.as_view()),
    path('news/', NewsList.as_view()),
    path('news/<int:pk>/', NewsDetail.as_view()),
    path('notifications/', NotificationList.as_view()),
    path('notifications/<int:pk>/', NotificationDetail.as_view)
]


