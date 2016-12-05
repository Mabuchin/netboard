from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^device_mon/', include('device_mon.urls', namespace='device_mon'))
]
