import shlex  
from subprocess import Popen, PIPE, STDOUT
import json

import requests

def get_simple_cmd_output(cmd, stderr=STDOUT):
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]

def get_ping_time(host):
    if not(host) :
        return 0
    
    print(host)
    host = host.split(':')[0]
    cmd = "fping {host} -C 1 -q".format(host=host)
    res = [float(x) for x in get_simple_cmd_output(cmd).strip().split(':')[-1].split() if x != '-']
    if len(res) > 0:
        return sum(res) / len(res)
    else:
        return 999
    
def upload_ping_time(id, yn, elapse_time):
    data = {"label_id": id, "live_yn" : yn, "elpase_ss" : elapse_time} 
    # data = {"elpase_ms": "0.09", "label_id": "3", "live_yn": 'Y'}
    print(data)
    url = 'http://localhost:8080/ords/aws/mon/servers'
    res = requests.post(url, params=data)
    print(res)
    return res

def get_ip_list() :
    url = "http://localhost:8080/ords/aws/mon/servers"
    data = requests.get(url)
    return data.json()['items']

ip_lists = get_ip_list()
          
for item in ip_lists :
    label_id = item['label_id']
    ip = item['ip']
    elapse_time = get_ping_time(ip)
    print(label_id, ip, elapse_time)
    if elapse_time == 999:
        print( ip + " no")
        
        upload_ping_time(label_id, 'N', elapse_time)
    else :
        upload_ping_time(label_id, 'Y', elapse_time)
