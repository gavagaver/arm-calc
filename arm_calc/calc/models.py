from django.contrib.auth import get_user_model

from django.db import models

from account.models import Folder
from core.models import BaseModel

User = get_user_model()

MASS_OF_METER = {
    6: 0.222,
    8: 0.395,
    10: 0.617,
    12: 0.888,
    14: 1.210,
    16: 1.580,
    18: 2.000,
    20: 2.470,
    22: 2.980,
    25: 3.850,
    28: 4.830,
    32: 6.310,
    36: 7.990,
    40: 9.870,
}
MM_IN_M = 1000


class Element(BaseModel):
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Папка',
        blank=True,
        null=True,
    )
    engineer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Инженер',
        default=1,
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
        verbose_name='Диаметр, мм',
    )
    arm_class = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name='Класс арматуры',
    )
    length_1 = models.SmallIntegerField(
        verbose_name='Длина 1 уч., мм',
    )
    quantity_1 = models.SmallIntegerField(
        default=1,
        verbose_name='Кол-во 1 уч., шт',
    )
    length_2 = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Длина 2 уч., мм',
    )
    quantity_2 = models.SmallIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Кол-во 2 уч., шт',
    )
    length_3 = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Длина 3 уч., мм',
    )
    quantity_3 = models.SmallIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Кол-во 3 уч., шт',
    )
    length_4 = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Длина 4 уч., мм',
    )
    quantity_4 = models.SmallIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Кол-во 4 уч., шт',
    )
    quantity = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Кол-во, шт',
    )

    @property
    def length(self):
        lenght = self.quantity_1 * self.length_1
        if self.length_2:
            lenght += self.quantity_2 * self.length_2
        if self.length_3:
            lenght += self.quantity_3 * self.length_3
        if self.length_4:
            lenght += self.quantity_4 * self.length_4

        return round(lenght, 1)

    def mass_of_single_rod(self):
        """Mass of single rod as mass of meter multiplied by length.
        """
        return round(MASS_OF_METER.get(self.diameter) * self.length / MM_IN_M,
                     2)

    def mass_of_rods(self):
        """Mass of rods as mass of single rod multiplied by quantity.
        """
        return round(self.mass_of_single_rod() * self.quantity, 2)

    class Meta:
        verbose_name = 'Стержень'
        verbose_name_plural = 'Стержни'
        ordering = ('title',)
