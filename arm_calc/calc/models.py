from django.db import models

from core.models import User, BaseModel, ConstructionModel, CalcModel, \
    PartModel

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

    class Meta:
        verbose_name = 'Расчет армирования'
        verbose_name_plural = 'Расчеты армирования'


class Rod(PartModel):
    rods_calc = models.ForeignKey(
        RodsCalc,
        on_delete=models.CASCADE,
        related_name='rods',
        verbose_name='Армирование',
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
        element_of_rod = Element.objects.get(pk=self.element.pk)
        lenght = self.quantity_1 * self.length_1 / element_of_rod.measurement_scale
        if self.length_2:
            lenght += self.quantity_2 * self.length_2 / element_of_rod.measurement_scale
        if self.length_3:
            lenght += self.quantity_3 * self.length_3 / element_of_rod.measurement_scale
        if self.length_4:
            lenght += self.quantity_4 * self.length_4 / element_of_rod.measurement_scale

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
