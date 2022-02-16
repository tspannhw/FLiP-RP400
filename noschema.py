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
