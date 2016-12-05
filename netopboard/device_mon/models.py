#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class Device(models.Model):
    hostname = models.CharField('Hostname',max_length=255,unique = True,)
    management_ip = models.GenericIPAddressField('Management IP address',null = True,blank = True,)
    snmp_community = models.CharField('SNMP community',max_length = 255,null = True,blank = True,)
    os = models.CharField('OS',max_length = 255,)
    user = models.CharField('User Name',max_length = 255,null = True,blank = True,)
    password = models.CharField('User Password',max_length = 255,null = True,blank = True,)
    enable_password =  models.CharField('Enable Password',max_length = 255,null = True,blank = True,)
    status = models.PositiveIntegerField('Status',default = 0)

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __unicode__(self):
        return self.hostname
