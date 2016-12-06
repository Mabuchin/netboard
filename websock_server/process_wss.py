#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options ,parse_command_line
from datetime import datetime
import shlex, subprocess , time ,re , json ,threading

UNIX_LOADINT = '.1.3.6.1.4.1.2021.10.1.5.1'
JUNOS_CPU_USE = '.1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0'
JUNOS_MEM_USE = '.1.3.6.1.4.1.2636.3.1.13.1.11.9.1.0.0'
IOSXR_CPU_USE = '.1.3.6.1.4.1.9.9.109.1.1.1.1.7.2'
IOSXR_MEM_USE = '.1.3.6.1.4.1.9.9.221.1.1.1.1.18'
IOSXR_MEM_FREE = '.1.3.6.1.4.1.9.9.221.1.1.1.1.20'

SLEEP_TIME =20 # SNMPを取得する間隔

#WebSocketがListenするポートを指定
define("port", default = 8090,type = int)

class SendWebSocket(tornado.websocket.WebSocketHandler):

    snmp_cmd_mem_use = ''
    snmp_cmd_mem_total = ''
    snmp_cmd_cpu_use = ''

    def get_process(self,message):
        result={}

        if json.loads(message['data'])['type'] == 'hello':
            COMMUNITY = json.loads(message['data'])['value']['community']
            IP = json.loads(message['data'])['value']['ip']
            OS = json.loads(message['data'])['value']['os']
            if OS == 'JUNOS':
                oid_mem_use = UNIX_LOADINT
                oid_mem_free = None
                oid_cpu_use = UNIX_LOADINT
            elif OS == 'IOSXR':
                oid_mem_use = IOSXR_MEM_USE
                oid_mem_free = IOSXR_MEM_FREE
                oid_cpu_use = IOSXR_CPU_USE
            else:
                raise

            if OS == 'IOSXR':
                snmp_cmd_mem_use = 'snmpwalk -v 2c -c %s %s %s'%(COMMUNITY,IP,oid_mem_use)
                snmp_cmd_mem_free = 'snmpwalk -v 2c -c %s %s %s'%(COMMUNITY,IP,oid_mem_free)
            else:
                snmp_cmd_mem_use = 'snmpget -v 2c -c %s %s %s'%(COMMUNITY,IP,oid_mem_use)
            snmp_cmd_cpu_use = 'snmpget -v 2c -c %s %s %s'%(COMMUNITY,IP,oid_cpu_use)

            mem_use = int(self.exe_snmp(snmp_cmd_mem_use))
            if OS == 'IOSXR':
                mem_free = int(self.exe_snmp(snmp_cmd_mem_free))
                mem_use = int((float(mem_use) / float(mem_use+mem_free) ) * 100)
            cpu_use = int(self.exe_snmp(snmp_cmd_cpu_use))

        try:
            result.update({'cpu_use' : cpu_use/10 , 'mem_use' : mem_use*40/100})
            result.update({'timestamp' : time.mktime(datetime.now().timetuple())})
            print "mem_use : %d  cpu_use : %d"%(mem_use,cpu_use)
            self.write_message(json.dumps(result))
        except:
            print "Client is already disconnectted."

    #コネクションが確保されると呼び出されるイベント
    def open(self):
        print 'Session Opened. IP:' + self.request.remote_ip

    #ブラウザが閉じられた場合等，切断イベントが発生した場合のイベント
    def on_close(self):
        print "Session closed"

    #クライアントからメッセージが送られてくると呼び出されるイベント
    def on_message(self, message):
        if json.loads(message)['type'] == 'hello':
            #WebSocketではtime.timerは使えない．下記変数のCallBackで遅延を再現
            #SLEE_TIME秒後に後半のSNMPと通信処理を開始する
            tornado.ioloop.IOLoop.instance().call_later(SLEEP_TIME,self.get_process,{'data':message})

    def exe_snmp(self,snmp_command):
        split_command = shlex.split(snmp_command)
        exec_output = subprocess.check_output(split_command)
        r = re.compile("(.*)(: )(.*)")
        snmp_result = r.match(exec_output).group(3)
        return snmp_result

    #Trueにしないと明示されたホストからしか通信を受け付けない
    def check_origin(self, origin):
        return True

#指定したURIでWSへの接続要求を待ち受ける
app = tornado.web.Application([
    (r"/device_mon/procws/", SendWebSocket),
])

if __name__ == "__main__":
    parse_command_line()
    app.listen(options.port)
    mainloop = tornado.ioloop.IOLoop.instance()
    mainloop.start()#WebSocketServer起動
