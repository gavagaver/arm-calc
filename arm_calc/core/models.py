from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class BaseModel(models.Model):
    """Abstract model. Add title, create date and __str__ """
    STR_CHAR_COUNT = 15

    title = models.CharField(
        max_length=70,
        verbose_name='Название'
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name='Дата последнего изменения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.title[:self.STR_CHAR_COUNT] + "..."}'

    def save(self, *args, **kwargs):
        """
        Overriding the save method to store the object's update date.
        """
        self.update_date = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ConstructionModel(BaseModel):
    """Abstract model."""

    class Meta:
        abstract = True


class CalcModel(BaseModel):
    """Abstract model."""
    pass

    class Meta:
        abstract = True


class PartModel(BaseModel):
    """Abstract model."""
    pass

    class Meta:
        abstract = True
