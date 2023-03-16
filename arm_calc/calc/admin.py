from django.contrib import admin
from calc.models import Construction, Folder, Element, RodsCalc, Rod


class FolderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'create_date',
        'engineer',
    )
    search_fields = ('title',)
    list_filter = ('create_date',)
    list_editable = ('title',)
    empty_value_display = '-пусто-',


class ConstructionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('create_date',)
    empty_value_display = '-пусто-',


class ElementAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'create_date',
    )
    search_fields = ('title',)
    list_filter = ('create_date',)
    list_editable = ('title',)
    empty_value_display = '-пусто-',


class RodsCalcAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('create_date',)
    empty_value_display = '-пусто-',


class RodAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'create_date',
        'rods_calc',
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
    list_filter = ('create_date', 'rods_calc',)
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


admin.site.register(Construction, ConstructionAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(RodsCalc, RodsCalcAdmin)
admin.site.register(Rod, RodAdmin)
