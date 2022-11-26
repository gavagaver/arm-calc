from django.contrib import admin
from django.urls import path, include

from calc import views

app_name = 'calc'

urlpatterns = [
    path(
        '<int:element_id>/',
        views.element,
        name='element',
    ),
]
