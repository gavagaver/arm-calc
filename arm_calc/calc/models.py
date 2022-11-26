from django.contrib.auth import get_user_model

from django.db import models
from django.db.models import SmallIntegerField

from account.models import Folder
from core.models import BaseModel

User = get_user_model()


class Element(BaseModel):
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Папка',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'


class Rod(BaseModel):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='rods',
        verbose_name='Элемент',
    )
    diameter = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Диаметр',
    )
    arm_class = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Класс арматуры',
    )
    length = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Длина',
    )

    class Meta:
        verbose_name = 'Стержень'
        verbose_name_plural = 'Стержни'
