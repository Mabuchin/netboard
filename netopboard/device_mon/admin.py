from django.contrib import admin
from device_mon.models import Device

class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'hostname',
        'management_ip',
        'snmp_community',
        'os',
        'user',
        'snmp_community',
        'user',
        'password',
        'status',
    )

admin.site.register(Device, DeviceAdmin)