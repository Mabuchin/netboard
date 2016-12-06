#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from device_mon.models import Device
from device_mon.scripts.access_device import get_status , get_interface ,get_cmd

def device_list(request):
    context = {'devices':Device.objects.all().order_by('hostname')}
    return render(request, 'device_mon/index.html', context)

def device_status(request):
    device_id = int(request.POST['device_id'])
    device = Device.objects.get( pk = device_id )
    context = {
                    'device_id'      : device_id,
                    'hostname'       : device.hostname,
                    'os'             : device.os,
                    'ip'             : device.management_ip,
                    'community'      : device.snmp_community,
                    'status'         : get_status(device),
                    'interfaces'     :  get_interface(device),
                }
    return render(request,'device_mon/result.html',context)

#BGP/IF Reload
def reload_device_status(request,device_id):
    device = Device.objects.get( pk = device_id )
    status_result = get_status(device)
    context = {
            'status'   : status_result,
            }
    return render(request,'device_mon/reload_block.html',context)

#plain cmd exec
def get_cmd_response(request,device_id,cmd):
    if cmd == 'None':
        cmd_result = 'None'
    else:
        cmd = cmd.replace('_',' ') # replace : show_bgp_su -> show bgp su
        device = Device.objects.get( pk = device_id )
        cmd_result = get_cmd(device,cmd)
    context = {
            'cmd_response'   : cmd_result,
            }
    return render(request,'device_mon/cmd_modal.html',context)