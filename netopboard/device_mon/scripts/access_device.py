#! /usr/bin/env python
# -*- coding: utf-8 -*-

from device_mon.models import Device
from device_mon.scripts.ExecuteOperation import IOSXROperation, JUNOSOperation
import shlex, subprocess
import re

IFINDEX = '1.3.6.1.2.1.2.2.1.1'
IFDESCR = '1.3.6.1.2.1.2.2.1.2'
IFALIAS = '1.3.6.1.2.1.31.1.1.1.18'

def get_status( device ):
    os = device.os

    session = decide_os(device.management_ip,device.user,device.password,os)

    result={}
    result.update(session.get_log(50))
    result.update(session.get_interface_status())
    result.update(session.get_bgp_summary())
    session.exit_session()

    return result

def get_cmd( device,cmd ):
    os = device.os
    ip = device.management_ip.encode('utf-8')
    user_id = device.user.encode('utf-8')
    password = device.password.encode('utf-8')
    session = decide_os(device.management_ip,device.user,device.password,os)

    result={}
    result = session.any_cmd(cmd.encode('utf-8'))
    session.exit_session()

    return result


def decide_os(ip,user,password,os):
    if   os == 'JUNOS':
        session = JUNOSOperation(ip, user, password ,os)
    elif os == 'IOSXR':
        session = IOSXROperation(ip, user, password ,os)
    else:
        session = 'cannot read OS type'
    return session

def get_interface( device ):
    result = []
    if_indexes = []
    interfaces_list = []
    r = re.compile("(.*)(: )(.*)")
    ip = device.management_ip
    community = device.snmp_community

    snmp_command = 'snmpwalk -v 2c -c %s %s %s'%(community,ip,IFINDEX)
    split_snmp_command = shlex.split(snmp_command)
    if_indexes_str = subprocess.check_output(split_snmp_command).splitlines()
    for if_index_str in if_indexes_str:
        if_index_str = int(r.match(if_index_str).group(3))
        if_indexes.append(int(if_index_str))
        print "ifindex : %d"%int(if_index_str)

    for if_index in if_indexes:
        snmp_command = 'snmpwalk -v 2c -c %s %s %s.%d'%(community,ip,IFDESCR,if_index)
        split_snmp_command = shlex.split(snmp_command)
        if_name = subprocess.check_output(split_snmp_command)
        snmp_command = 'snmpwalk -v 2c -c %s %s %s.%d'%(community,ip,IFALIAS,if_index)
        split_snmp_command = shlex.split(snmp_command)
        if_descr = subprocess.check_output(split_snmp_command)
        if_name = r.match(if_name).group(3).strip('\\"')
        if_descr = r.match(if_descr).group(3).strip('\\"')
        interfaces_list.append({'name': if_name, 'descr': if_descr,'ifindex' : if_index})
    return interfaces_list
