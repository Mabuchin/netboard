# Netboard
This is Django application that monitors router in realtime.
It is possible to check BGP, Interface, CPU, Memory, Log, any command.
It corresponds to IOS-XR and JUNOS.

![dashboard_sample](https://raw.github.com/wiki/Mabuchin/netboard/image/netboard_sample.png)

# How to use

 1. Get highchart and put under `/netopboard/device_mon/static/device_mon/`

    http://www.highcharts.com/
    *It is a free license for individual use only.
 2. Installing using pip
 
    `pip install -r require.txt`
 3. Django migrate database
 
    `python manage.py migrate`
 4. Launch netopboard
 
    `nginx`+`uwsgi`,or `python manage.py runserver 0.0.0.0:8000`
 5. Input device data

    Let's access Netboard's admin page.
    Input the target device information.
    `http://yourdomain/admin/`
 6. Rewrite `device_mon/templates/device_mon/result.html`

    ```
        var ws_proc_url = "ws://localhost:8090/device_mon/procws/" //Rewrite to your URL
        var ws_tr_url = "ws://localhost:8080/device_mon/trws/" //Rewrite to your URL
    ```
 7. Launch WebsocketServer

    LISTEN 8080 and 8090 ports.
    ```
    cd websock_server
    nohup python if_traffic_wss.py &
    nohup python process_wss.py &
    ```
