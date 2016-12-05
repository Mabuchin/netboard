from django.conf.urls import url
from device_mon import views

urlpatterns = [
    url(r'^$',views.device_list, name='index'),
    url(r'^result/$', views.device_statuses, name='result')
    #url(r'^status/(?P<router_id>\d+)$', views.device, name='router_api'),
    #url(r'^cmd_response/(?P<router_id>\d+)/(?P<plain_cmd>.+)$', views.get_cmd_response, name='cmd_response')
]