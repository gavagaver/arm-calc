from django.contrib.auth import get_user_model

from django.db import models
from core.models import BaseModel

User = get_user_model()


class Element(BaseModel):
    engineer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Инженер',
    )

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'


class Rod(BaseModel):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='rods',
        verbose_name='Стержень',
    )

    class Meta:
        verbose_name = 'Стержень'
        verbose_name_plural = 'Стержни'
