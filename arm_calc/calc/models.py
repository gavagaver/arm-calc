from django.db import models

from core.models import User, BaseModel, ConstructionModel, CalcModel, \
    PartModel


class Site(BaseModel):
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
    measurement_scale = models.SmallIntegerField(
        default=1,
        verbose_name='Масштаб измерений',
        help_text='Во сколько раз вводимые значения больше действительных'
    )

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'


class RodsCalc(CalcModel):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='rods_calcs',
        verbose_name='Элемент',
    )
    total_mass = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Всего, кг',
    )

    class Meta:
        verbose_name = 'Расчет армирования'
        verbose_name_plural = 'Расчеты армирования'


class RodClass(BaseModel):
    rods_calc = models.ForeignKey(
        RodsCalc,
        on_delete=models.CASCADE,
        related_name='rod_classes',
        verbose_name='Армирование',
    )
    total_mass = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Всего, кг',
    )


class RodDiameter(BaseModel):
    rod_class = models.ForeignKey(
        RodClass,
        on_delete=models.CASCADE,
        related_name='rod_diameters',
        verbose_name='Класс арматуры',
    )
    total_mass = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Всего, кг',
    )


class Rod(PartModel):
    rods_calc = models.ForeignKey(
        RodsCalc,
        on_delete=models.CASCADE,
        related_name='rods',
        verbose_name='Армирование',
    )
    diameter = models.ForeignKey(
        RodDiameter,
        on_delete=models.CASCADE,
        related_name='rods',
        verbose_name='Диаметр, мм',
    )
    rod_class = models.ForeignKey(
        RodClass,
        on_delete=models.CASCADE,
        related_name='rods',
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
    length = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Длина, м',
    )
    mass_of_single_rod = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Масса стержня, кг',
    )
    mass_of_rods = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Масса позиции, м',
    )

    class Meta:
        verbose_name = 'Стержень'
        verbose_name_plural = 'Стержни'
        ordering = ('title',)


class VolumesCalc(CalcModel):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='volumes_calcs',
        verbose_name='Элемент',
    )

    class Meta:
        verbose_name = 'Расчет объема'
        verbose_name_plural = 'Расчеты объемов'


class Volume(PartModel):
    volumes_calc = models.ForeignKey(
        VolumesCalc,
        on_delete=models.CASCADE,
        related_name='volumes',
        verbose_name='Расчет объема',
    )


class SquaresCalc(CalcModel):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='squares_calcs',
        verbose_name='Элемент',
    )

    class Meta:
        verbose_name = 'Расчет площади'
        verbose_name_plural = 'Расчеты площадей'


class Square(PartModel):
    squares_calc = models.ForeignKey(
        SquaresCalc,
        on_delete=models.CASCADE,
        related_name='squares',
        verbose_name='Расчет площади',
    )


class LengthsCalc(CalcModel):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='lengths_calcs',
        verbose_name='Элемент',
    )

    class Meta:
        verbose_name = 'Расчет длины'
        verbose_name_plural = 'Расчеты длин'


class Length(PartModel):
    lengths_calc = models.ForeignKey(
        LengthsCalc,
        on_delete=models.CASCADE,
        related_name='lengths',
        verbose_name='Расчет длины',
    )


class UnitsCalc(CalcModel):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='units_calcs',
        verbose_name='Элемент',
    )

    class Meta:
        verbose_name = 'Расчет единиц'
        verbose_name_plural = 'Расчеты единиц'


class Unit(PartModel):
    units_calc = models.ForeignKey(
        UnitsCalc,
        on_delete=models.CASCADE,
        related_name='units',
        verbose_name='Расчет единиц',
    )
