# myapp/models.py
from django.db import models

class UploadedXLSX(models.Model):
    xlsx_file = models.FileField(upload_to='uploads/')
    client_ip = models.GenericIPAddressField()

    def __str__(self):
        return str(self.xlsx_file)

