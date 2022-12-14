from django.contrib.auth import get_user_model

from django.db import models
from core.models import BaseModel

User = get_user_model()


class Folder(BaseModel):
    engineer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='folders',
        verbose_name='Инженер',
    )

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'
