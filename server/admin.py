from django.contrib import admin

from . import models


class GuitarSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link')


# Register your models here.
admin.site.register(models.GuitarSheet, GuitarSheetAdmin)
