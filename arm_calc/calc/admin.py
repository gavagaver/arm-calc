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
    )
    search_fields = ('title',)
    list_filter = ('create_date',)
    list_editable = ('title',)
    empty_value_display = '-пусто-',


admin.site.register(Element, ElementAdmin)
admin.site.register(Rod, RodAdmin)
