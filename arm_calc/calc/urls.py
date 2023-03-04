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
        'create_rods_calc/',
        views.RodsCalcCreate.as_view(),
        name='create_rods_calc',
    ),
    path(
        'create_element/',
        views.create_element,
        name='create_element',
    ),
    path(
        'update_rods_calc/<int:pk>/',
        views.RodsCalcUpdate.as_view(),
        name='update_rods_calc',
    ),
    path(
        'update_element/<int:pk>/',
        views.update_element,
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
    path(
        'copy-rod/<int:pk>/',
        views.copy_rod,
        name='copy_rod',
    ),
    path(
        'copy-element/<int:pk>/',
        views.copy_element,
        name='copy_element',
    ),
]
