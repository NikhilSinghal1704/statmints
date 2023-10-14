from django.contrib import admin
from .models import UploadedXLSX

class UploadedXLSXAdmin(admin.ModelAdmin):
    list_display = ('xlsx_file', 'client_ip')

# Register the model and admin class
admin.site.register(UploadedXLSX, UploadedXLSXAdmin)

