from django.contrib import admin
from django.urls import path, include

from account import views

app_name = 'account'

urlpatterns = [
    path(
        '',
        views.landing,
        name='landing',
    ),
    path(
        'folder/<int:folder_id>/',
        views.folder,
        name='list_elements',
    ),
    path(
        'create_folder/',
        views.create_folder,
        name='create_folder',
    ),
    path(
        'profile/<str:username>/',
        views.profile,
        name='profile',
    ),
]
