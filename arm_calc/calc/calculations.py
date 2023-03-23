from . import models

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


def calculate_rod(rod):

    element = models.Element.objects.get(pk=rod.rods_calc.element.pk)
    length = rod.quantity_1 * rod.length_1 / element.measurement_scale
    if rod.length_2:
        length += rod.quantity_2 * rod.length_2 / element.measurement_scale
    if rod.length_3:
        length += rod.quantity_3 * rod.length_3 / element.measurement_scale
    if rod.length_4:
        length += rod.quantity_4 * rod.length_4 / element.measurement_scale
    rod.length = round(length, 1)

    rod.mass_of_single_rod = round(MASS_OF_METER.get(rod.diameter) * rod.length / MM_IN_M, 2)

    rod.mass_of_rods = round(rod.mass_of_single_rod() * rod.quantity, 2)

    rod.save()
