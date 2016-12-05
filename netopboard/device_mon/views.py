#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from device_mon.models import Device

def device_list(request):
    return render(request, 'device_mon/index.html', dict(devices=Device.objects.all().order_by('hostname')))

def device_statuses(request):
    return redirect('device_mon:index')
