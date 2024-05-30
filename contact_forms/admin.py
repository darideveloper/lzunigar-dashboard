import csv
from django.contrib import admin
from contact_forms import models
from django.http import HttpResponse


@admin.register(models.GanoConCocaCola)
class GanoConCocaColaAdmin(admin.ModelAdmin):
    
    def export_csv(self, request, queryset):
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'id',
            'nombre',
            'email',
            'telefono',
            'fecha_creacion',
            'fecha_actualizacion'
        ])
        
        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.nombre,
                obj.email,
                obj.telefono,
                obj.created_at,
                obj.updated_at
            ])
        
        return response
    
    export_csv.short_description = 'Exportar a CSV'
    
    list_display = ('id', 'nombre', 'email', 'telefono', 'created_at', 'updated_at')
    search_fields = ('nombre', 'email', 'telefono', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    actions = ['export_csv']