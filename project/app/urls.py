from django.contrib.auth.decorators import login_required

from django.urls import path
from django.contrib.auth import views as auth_views, views
from .views import *
   




urlpatterns = [
    
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


    