import time
from icp10125 import ICP10125
from mics6814 import MICS6814
import logging
import pulsar
import sys
import datetime
import subprocess
import os
import traceback
import math
import base64
import json
from time import gmtime, strftime
import random, string
import time
import psutil
import uuid
from time import sleep
from math import isnan
from subprocess import PIPE, Popen
import socket 
from pulsar.schema import *

### Schema Object
# https://pulsar.apache.org/docs/en/client-libraries-python/

class rp400(Record):
    uuid = String()
    ipaddress = String()
    cputempf = Integer()
    runtime = Integer()
    host = String()
    hostname = String()
    macaddress = String()
    endtime = String()
    te = String()
    cpu = Float()
    diskusage = String()
    memory = Float()
    rowid = String()
    systemtime = String()
    ts = Integer()
    starttime = String()
    pressure = Float()
    temperature = Float()
    gasoxidising = Float()
    gasadc = Float()
    gasreducing = Float()
    gasnh3 = Float()

### Build Objects

device = ICP10125()
gas = MICS6814()
gas.set_led(0,0,0)   # turn off light

client = pulsar.Client('pulsar://pulsar1:6650')
producer = client.create_producer(topic='persistent://public/default/rp400' ,schema=JsonSchema(rp400),properties={"producer-name": "rp400-py-sensor","producer-id": "rp400-sensor" })

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

# IP Address
def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

# Get MAC address of a local interfaces
def psutil_iface(iface):
    # type: (str) -> Optional[str]
    import psutil
    nics = psutil.net_if_addrs()
    if iface in nics:
        nic = nics[iface]
        for i in nic:
            if i.family == psutil.AF_LINK:
                return i.address
# Random Word
def randomword(length):
 return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()) for i in range(length))

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

# Timer
packet_size=3000

# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
factor = 2.25

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name) 
ipaddress = IP_address()

try:
    while True:
        currenttime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        starttime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        start = time.time()

        # Create unique id
        uniqueid = 'uuid_{0}_{1}'.format(randomword(3),strftime("%Y%m%d%H%M%S",gmtime()))
        uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
        pressure, temperature = device.measure()

        # CPU Temp
        f = open("/sys/devices/virtual/thermal/thermal_zone0/temp","r")
        cputemp = str( f.readline() )
        cputemp = cputemp.replace('\n','')
        cputemp = cputemp.strip()
        cputemp = str(round(float(cputemp)) / 1000)
        cputempf = str(round(9.0/5.0 * float(cputemp) + 32))
        f.close()

        usage = psutil.disk_usage("/")
        end = time.time()

        rp400Record = rp400()
        rp400Record.uuid = uniqueid
        rp400Record.ipaddress = ipaddress
        rp400Record.cputempf = int(cputempf)
        rp400Record.runtime =  int(round(end - start)) 
        rp400Record.host = os.uname()[1]
        rp400Record.hostname = host_name
        rp400Record.macaddress = psutil_iface('wlan0')
        rp400Record.endtime = '{0}'.format( str(end ))
        rp400Record.te = '{0}'.format(str(end-start))
        rp400Record.cpu = psutil.cpu_percent(interval=1)
        rp400Record.diskusage = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
        rp400Record.memory = psutil.virtual_memory().percent
        rp400Record.rowid = str(uuid2)
        rp400Record.systemtime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        rp400Record.ts =  int( time.time() )
        rp400Record.starttime = str(starttime)
        rp400Record.pressure = round(pressure,2)
        rp400Record.temperature = round(temperature,2)
        rp400Record.gasoxidising =  round(gas.read_all().oxidising,2)
        rp400Record.gasadc = round(gas.read_all().adc,2)
        rp400Record.gasreducing = round(gas.read_all().reducing,2)
        rp400Record.gasnh3 = round(gas.read_all().nh3,2)
        print(rp400Record)
        producer.send(rp400Record,partition_key=uniqueid)
        #row = { }
        #row['uuid'] =  uniqueid
       # row['ipaddress']=ipaddress
        #row['cputempf'] =  cputempf
        #row['runtime'] = str(round(end - start)) 
        #row['host'] = os.uname()[1]
        #row['hostname'] = host_name
        #row['macaddress'] = psutil_iface('wlan0')
        #row['endtime'] = '{0}'.format( str(end ))
        #row['te'] = '{0}'.format(str(end-start))
        #row['cpu'] = psutil.cpu_percent(interval=1)
        #row['diskusage'] = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
        #row['memory'] = psutil.virtual_memory().percent
        #row['rowid'] = str(uuid2)
        #row['systemtime'] = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        #row['ts'] = int( time.time() )
        #row['starttime'] = str(starttime)
       #row['pressure'] = round(pressure,2)
        #row['temperature'] = round(temperature,2)
        #row['gasoxidising'] = round(gas.read_all().oxidising,2)
        #row['gasadc'] = round(gas.read_all().adc,2)
        #row['gasreducing'] = round(gas.read_all().reducing,2)
        #row['gasnh3'] = round(gas.read_all().nh3,2)
        #json_string = json.dumps(row)
        #json_string = json_string.strip()
        #print(json_string)
        # producer.send(Example(a='Hello', b=1))
        #producer.send((json_string).encode('utf-8'))
except KeyboardInterrupt:
    pass

client.flush()
client.close()
