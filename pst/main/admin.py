from django.contrib import admin
from .models import DataPing, DataPingstatistics, DataSpeedtest

# Register your models here.
admin.site.register(DataPing)
admin.site.register(DataPingstatistics)
admin.site.register(DataSpeedtest)