from django.contrib import admin
from contact_forms import models


@admin.register(models.GanoConCocaCola)
class GanoConCocaColaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'created_at', 'updated_at')
    search_fields = ('nombre', 'email', 'telefono', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')