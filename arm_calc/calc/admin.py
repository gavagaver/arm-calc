from django.contrib import admin
from calc.models import Element, Rod


class ElementAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'create_date',
        'folder',
    )
    search_fields = ('title',)
    list_filter = ('create_date',)
    list_editable = ('title',)
    empty_value_display = '-пусто-',


class RodAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'create_date',
        'element',
        'diameter',
        'arm_class',
        'length_1',
        'quantity_1',
        'length_2',
        'quantity_2',
        'length_3',
        'quantity_3',
        'length_4',
        'quantity_4',
        'quantity',
        'mass_of_single_rod',
        'mass_of_rods',
    )
    search_fields = ('title',)
    list_filter = ('create_date', 'element',)
    list_editable = (
        'title',
        'diameter',
        'arm_class',
        'length_1',
        'quantity_1',
        'length_2',
        'quantity_2',
        'length_3',
        'quantity_3',
        'length_4',
        'quantity_4',
        'quantity',
    )
    empty_value_display = '-пусто-',


admin.site.register(Element, ElementAdmin)
admin.site.register(Rod, RodAdmin)
