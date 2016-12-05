#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from device_mon.models import Device
import pyping


class Command(BaseCommand):
    def handle(self, *args, **options):

        devices = Device.objects.all()

        for device in devices:
            response = pyping.ping(device.management_ip, count=1, timeout=1000)
            if response.ret_code == 0:
                device.status = 1
            else:
                device.status = 0

            device.save()

        # loss_pat='0 received'
        # msg_pat='icmp_seq=0'
        # for device in devices:
        #     try:
        #         management_ip = device.management_ip
        #         ping = subprocess.Popen(
        #             ["ping", "-c", "1" , "-W" , "1" , management_ip],
        #             stdout = subprocess.PIPE,
        #             stderr = subprocess.PIPE
        #         )
        #         out, error = ping.communicate()
        #         for line in out.splitlines():
        #             if line.find(msg_pat)>-1:
        #                 flag=True
        #                 break
        #             else:
        #                 flag=False
        #     except TypeError:
        #         flag=False