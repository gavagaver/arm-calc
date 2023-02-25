from django.contrib import admin
from django.urls import path, include

from account import views

app_name = 'account'

urlpatterns = [
    path(
        'folder/<int:pk>/',
        views.folder,
        name='list_elements',
    ),
    path(
        'folder/',
        views.folder,
        name='folder',
    ),
]
