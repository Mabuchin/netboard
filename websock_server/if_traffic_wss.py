#! /usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options ,parse_command_line
from datetime import datetime
import shlex, subprocess , time ,re , json ,threading

OID_IFHCINOCTET_IN = '1.3.6.1.2.1.31.1.1.1.6'
OID_IFHCINOCTET_OUT = '1.3.6.1.2.1.31.1.1.1.10'
SLEEP_TIME =10

#WebSocketがListenするポートを指定
define("port", default = 8080,type = int)

class SendWebSocket(tornado.websocket.WebSocketHandler):

    #コネクションが確保されると呼び出されるイベント
    def open(self):
        print 'Session Opened. IP:' + self.request.remote_ip

    #ブラウザが閉じられた場合等，切断イベントが発生した場合のイベント
    def on_close(self):
        print "Session closed"

    #クライアントからメッセージが送られてくると呼び出されるイベント
    def on_message(self, message):
        if json.loads(message)['type'] == 'hello':
            COMMUNITY = json.loads(message)['value']['community']
            IP = json.loads(message)['value']['ip']
            IFINDEX = json.loads(message)['value']['ifindex']
            snmp_command_in = 'snmpget -v 2c -c %s %s %s.%s'%(COMMUNITY,IP,OID_IFHCINOCTET_IN,IFINDEX)
            snmp_command_out = 'snmpget -v 2c -c %s %s %s.%s'%(COMMUNITY,IP,OID_IFHCINOCTET_OUT,IFINDEX)
            pre_counter_in = int(self.exe_snmp(snmp_command_in))*8
            pre_counter_out = int(self.exe_snmp(snmp_command_out))*8

            tornado.ioloop.IOLoop.instance().call_later(SLEEP_TIME,self.snmp_second_half,
                                                        {
                                                        'snmp_command_in':snmp_command_in,
                                                        'snmp_command_out':snmp_command_out,
                                                        'in_counter':pre_counter_in,
                                                        'out_counter':pre_counter_out,
                                                        })

    #SLEEP_TIME秒後のSNMPを取得
    def snmp_second_half(self,pre_inf):
        result = {}
        pos_counter_in = int(self.exe_snmp(pre_inf['snmp_command_in']))*8
        pos_counter_out = int(self.exe_snmp(pre_inf['snmp_command_out']))*8

        #指定秒数とのcounter差分からトラフィック算出
        traffic_in = (pos_counter_in - pre_inf['in_counter'])  / SLEEP_TIME
        traffic_out = (pos_counter_out - pre_inf['out_counter'])  / SLEEP_TIME
        #JSON化したトラフィックデータをWebクライアントへ送信
        try:
            result.update({'traffic_in' : traffic_in , 'traffic_out' : traffic_out})
            result.update({'timestamp' : time.mktime(datetime.now().timetuple())})
            print "traffic(in) : %d  traffic(out) : %d [pos_counter_in : %d , pos_counter_out : %d]"%(traffic_in,traffic_out,pos_counter_in,pos_counter_out)
            self.write_message(json.dumps(result))
        except:
            print "Client is already disconnectted."

    #SNMP実行結果のValueのみを返す
    #e.g. [IF-MIB::ifHighSpeed.21 = Gauge32: 1000] -> [1000]
    def exe_snmp(self,snmp_command):
        split_command = shlex.split(snmp_command)
        exec_output = subprocess.check_output(split_command)
        r = re.compile("(.*)(: )(.*)")
        snmp_result = r.match(exec_output).group(3)
        return snmp_result

    def check_origin(self, origin):
        return True

#指定したURIでWSへの接続要求を待ち受ける
app = tornado.web.Application([
    (r"/device_mon/trws/", SendWebSocket),
])

if __name__ == "__main__":
    parse_command_line()
    app.listen(options.port)
    mainloop = tornado.ioloop.IOLoop.instance()
    mainloop.start()
