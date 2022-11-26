from django.contrib import admin
from account.models import Folder


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


admin.site.register(Folder, FolderAdmin)
