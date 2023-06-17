from django.contrib import admin

from . import models


class SiteAdmin:
    """
    Admin configuration for Site model.
    """
    list_display = ('title', 'engineer')
    search_fields = ('title',)
    list_filter = ('create_date',)
    empty_value_display = '-пусто-',


class ConstructionAdmin:
    """
    Admin configuration for Construction model.
    """
    list_display = ('title', 'site')
    search_fields = ('title',)
    list_filter = ('create_date',)
    empty_value_display = '-пусто-',


class VersionAdmin:
    """
    Admin configuration for Version model.
    """
    list_display = ('title', 'construction')
    search_fields = ('title',)
    list_filter = ('create_date',)
    empty_value_display = '-пусто-',


class ElementAdmin:
    """
    Admin configuration for Element model.
    """
    list_display = (
        'pk',
        'title',
        'create_date',
    )
    search_fields = ('title',)
    list_filter = ('create_date',)
    list_editable = ('title',)
    empty_value_display = '-пусто-',


class FolderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Folder model.
    """
    list_display = (
        'pk',
        'title',
        'create_date',
        'version',
    )
    search_fields = ('title',)
    list_filter = ('create_date',)
    list_editable = ('title',)
    empty_value_display = '-пусто-',


class RodsCalcAdmin(admin.ModelAdmin):
    """
    Admin configuration for RodsCalc model.
    """
    list_display = ('title', 'element', 'total_mass')
    search_fields = ('title',)
    list_filter = ('create_date',)
    empty_value_display = '-пусто-',


class RodClassAdmin(admin.ModelAdmin):
    """
    Admin configuration for RodClass model.
    """
    list_display = ('rods_calc', 'title', 'total_mass')
    empty_value_display = '-пусто-',


class RodDiameterAdmin(admin.ModelAdmin):
    """
    Admin configuration for RodDiameter model.
    """
    list_display = ('rod_class', 'title', 'total_mass')
    empty_value_display = '-пусто-',


class RodAdmin(admin.ModelAdmin):
    """
    Admin configuration for Rod model.
    """
    list_display = (
        'pk',
        'title',
        'create_date',
        'rods_calc',
        'diameter',
        'rod_class',
        'length_1',
        'quantity_1',
        'length_2',
        'quantity_2',
        'length_3',
        'quantity_3',
        'quantity',
        'length',
        'mass_of_single_rod',
        'mass_of_rods',
    )
    search_fields = ('title',)
    list_filter = ('create_date', 'rods_calc',)
    list_editable = (
        'title',
        'rods_calc',
        'diameter',
        'rod_class',
        'length_1',
        'quantity_1',
        'length_2',
        'quantity_2',
        'length_3',
        'quantity_3',
        'quantity',
        'length',
        'mass_of_single_rod',
        'mass_of_rods',
    )
    empty_value_display = '-пусто-',


admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Construction, ConstructionAdmin)
admin.site.register(models.Version, VersionAdmin)
admin.site.register(models.Folder, FolderAdmin)
admin.site.register(models.Element, ElementAdmin)
admin.site.register(models.RodsCalc, RodsCalcAdmin)
admin.site.register(models.RodClass, RodClassAdmin)
admin.site.register(models.RodDiameter, RodDiameterAdmin)
admin.site.register(models.Rod, RodAdmin)
