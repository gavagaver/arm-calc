from core.models import (BaseModel, CalcModel, ConstructionModel, PartModel,
                         User)
from django.db import models

from . import calculation_settings as calc


class Site(BaseModel):
    """
    Model for representing a site.
    A site is a project that contains constructions.
    """
    engineer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sites',
        verbose_name='Инженер',
    )

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Construction(ConstructionModel):
    """
    Model for representing a construction, which belongs to a site.
    """
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='constructions',
        verbose_name='Объект',
        default=1,
    )

    class Meta:
        verbose_name = 'Сооружение'
        verbose_name_plural = 'Сооружения'


class Version(BaseModel):
    """
    Model for representing a version of a construction.
    """
    construction = models.ForeignKey(
        Construction,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='Сооружение',
    )

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


class Folder(BaseModel):
    """
    Model for representing a folder containing elements within a version.
    """
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        related_name='folders',
        verbose_name='Версия',
    )

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'


class Element(BaseModel):
    """
    Model for representing an element, which belongs to a folder.
    """
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Папка',
    )
    engineer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Инженер',
    )

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'


class RodsCalc(CalcModel):
    """
    Model for representing a calculation of reinforcement for an element.
    """
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='rods_calcs',
        verbose_name='Элемент',
    )
    total_mass = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Всего, кг',
    )
    measurement_scale = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Масштаб измерений',
        help_text='Во сколько раз вводимые значения больше действительных'
    )

    class Meta:
        verbose_name = 'Расчет армирования'
        verbose_name_plural = 'Расчеты армирования'


class RodClass(BaseModel):
    """
    Model for representing a class of reinforcement for a calculation.
    """
    rods_calc = models.ForeignKey(
        RodsCalc,
        on_delete=models.CASCADE,
        related_name='rod_classes',
        verbose_name='Армирование',
    )
    total_mass = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Всего, кг',
    )


class RodDiameter(BaseModel):
    """
    Model for representing a diameter of reinforcement rod.
    """
    rod_class = models.ForeignKey(
        RodClass,
        on_delete=models.CASCADE,
        related_name='rod_diameters',
        verbose_name='Класс арматуры',
    )
    total_mass = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Всего, кг',
    )


class Rod(PartModel):
    """
    Model for representing a single reinforcement rod.
    """
    rods_calc = models.ForeignKey(
        RodsCalc,
        on_delete=models.CASCADE,
        related_name='rods',
        verbose_name='Армирование',
    )
    diameter = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='⌀',
    )
    rod_class = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name='Класс',
    )
    length_1 = models.PositiveIntegerField(
        verbose_name='Длина A, мм',
    )
    quantity_1 = models.PositiveIntegerField(
        default=1,
        verbose_name='Кол-во n1, шт',
    )
    length_2 = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Длина B, мм',
    )
    quantity_2 = models.PositiveIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Кол-во n2, шт',
    )
    length_3 = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Длина C, мм',
    )
    quantity_3 = models.PositiveIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Кол-во n3, шт',
    )
    quantity_a = models.PositiveIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Множитель F, шт',
    )
    quantity_b = models.PositiveIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Множитель G, шт',
    )
    quantity_c = models.PositiveIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name='Множитель H, шт',
    )
    quantity = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Кол-во, шт',
    )
    length = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Длина, мм',
    )
    mass_of_single_rod = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Масса стержня, кг',
    )
    mass_of_rods = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Масса позиции, кг',
    )

    def save(self, *args, **kwargs):
        self.calculate_fields()
        self.calculate_mass_of_single_rod()
        self.calculate_mass_of_rods()
        super(Rod, self).save(*args, **kwargs)

    def calculate_fields(self):
        """
        Calculates the length and quantity of the reinforcement rod
        based on lengths and quantities of different sections
        and quantities a, b, c.
        """
        rods_calc = RodsCalc.objects.get(pk=self.rods_calc.pk)

        length = self.quantity_1 * self.length_1
        if self.length_2:
            length += self.quantity_2 * self.length_2
        if self.length_3:
            length += self.quantity_3 * self.length_3
        self.length = round(length, calc.NUM_OF_DECIMALS)

        quantity = self.quantity_a * self.quantity_b * self.quantity_c
        self.quantity = round(quantity, calc.NUM_OF_DECIMALS_OF_INTEGER)

    def calculate_mass_of_single_rod(self):
        """
        Calculates the mass of a single reinforcement rod
        based on its length and diameter.
        """
        self.mass_of_single_rod = (
            calc.MASS_OF_METER.get(self.diameter)
            * self.length / calc.MM_IN_M
        )

    def calculate_mass_of_rods(self):
        """
        Calculates the total mass of the reinforcement rods
        based on the mass of a single rod and its quantity.
        """
        self.mass_of_rods = round(
            self.mass_of_single_rod * self.quantity,
            calc.NUM_OF_DECIMALS,
        )

    class Meta:
        verbose_name = 'Стержень'
        verbose_name_plural = 'Стержни'
        ordering = ('title',)
