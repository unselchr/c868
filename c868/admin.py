from django.contrib import admin
from . import models as models

admin.site.register(models.Role)
admin.site.register(models.Part)