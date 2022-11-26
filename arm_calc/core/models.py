from django.db import models


class BaseModel(models.Model):
    """Abstract model. Add title, create date and __str__ """
    STR_CHAR_COUNT = 15

    title = models.CharField(
        max_length=150,
        verbose_name='Название'
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.title[:self.STR_CHAR_COUNT] + "..."}'

    class Meta:
        abstract = True
