from django.contrib import admin
from django.urls import path, include

from calc import views

app_name = 'calc'

urlpatterns = [
    path(
        'result/<int:pk>/',
        views.result,
        name='result',
    ),
    path(
        'create/',
        views.ElementCreate.as_view(),
        name='create_element',
    ),
    path(
        'update/<int:pk>/',
        views.ElementUpdate.as_view(),
        name='update_element',
    ),
    path(
        'delete/<int:pk>/',
        views.delete_element,
        name='delete_element',
    ),
    path(
        'delete-rod/<int:pk>/',
        views.delete_rod,
        name='delete_rod',
    ),
]
