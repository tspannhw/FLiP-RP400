## FLiP-RP400

Raspberry pi 400 plus breakoutgarden


### References

* https://shop.pimoroni.com/products/breakout-garden-400
* https://github.com/pimoroni/breakout-garden/tree/master/examples
* https://shop.pimoroni.com/products/icp10125-air-pressure-breakout
* https://github.com/pimoroni/icp10125-python
* https://shop.pimoroni.com/products/1-12-oled-breakout?variant=12628508704851
* https://shop.pimoroni.com/products/mics6814-gas-sensor-breakout
* https://github.com/pimoroni/mics6814-python



### Sensors

* TDK InvenSense ICP-10125 Barometric Pressure and Temperature Sensor - I2C
* 1.12" Mono OLED (128x128, white/black) Breakout – SPI
* MICS6814 3-in-1 Gas Sensor Breakout (CO, NO2, NH3) - I2C

### Consume Data

````

bin/pulsar-client consume "persistent://public/default/rp400" -s "rp400reader" -n 0

----- got message -----
key:[uuid_uwm_20220216193457], properties:[], content:{
 "uuid": "uuid_uwm_20220216193457",
 "ipaddress": "192.168.1.236",
 "cputempf": 93,
 "runtime": 0,
 "host": "rp400",
 "hostname": "rp400",
 "macaddress": "e4:5f:01:1d:69:db",
 "endtime": "1645040097.7178762",
 "te": "0.009049177169799805",
 "cpu": 14.0,
 "diskusage": "48124.5 MB",
 "memory": 6.2,
 "rowid": "20220216193457_530e17a4-7aed-4b4f-920f-310feeb71784",
 "systemtime": "02/16/2022 14:34:58",
 "ts": 1645040098,
 "starttime": "02/16/2022 14:34:57",
 "pressure": 102864.29,
 "temperature": 23.43,
 "gasoxidising": 32540.54,
 "gasadc": 3.23,
 "gasreducing": 214106.01,
 "gasnh3": 101500.0
}

````
