from django.conf.urls import url
from device_mon import views

urlpatterns = [
    url(r'^$',views.device_list, name='index'),
    url(r'^result/$', views.device_status, name='result'),
    url(r'^reload/(?P<device_id>\d+)$', views.reload_device_status, name='reload'),
    url(r'^cmd_response/(?P<device_id>\d+)/(?P<cmd>.+)$', views.get_cmd_response, name='cmd_response')
]