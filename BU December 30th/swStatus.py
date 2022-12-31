#Controlling and monitoring Tuya devices on your network requires the following:

#	Address - The network address (IPv4) of the device e.g. 10.0.1.100
#	Device ID - The unique identifier for the Tuya device
#	Version - The Tuya protocol version used (3.1 or 3.3)
#	Local_Key - The security key required to access the Tuya device.

#Installed using: pip3 install tinytuya
#Using: python3 -m tinytuya scan

#produced:
#	Scanning on UDP ports 6666 and 6667 for devices (15 retries)...

#'Unknown v3.4 Device   Product ID = keyjnuy4s3kre7m7  [Valid payload]:
#    Address = 192.168.10.101,  Device ID = bf5723e4b65de4a64fteqz, Local Key = ,  Version = 3.4, MAC = 
#    No Stats for 192.168.10.101: DEVICE KEY required to poll for status

#Unknown v3.4 Device   Product ID = keyjnuy4s3kre7m7  [Valid payload]:
#    Address = 192.168.10.122,  Device ID = bfae7fdb0b0c3c03522yoo, Local Key = ,  Version = 3.4, MAC = 
#    No Stats for 192.168.10.122: DEVICE KEY required to poll for status

#Unknown v3.4 Device   Product ID = keyjnuy4s3kre7m7  [Valid payload]:
#    Address = 192.168.10.165,  Device ID = bf0e00da7f4df8c38dxvqu, Local Key = ,  Version = 3.4, MAC = 
#    No Stats for 192.168.10.165: DEVICE KEY required to poll for status


# Used PDF instructions here to set uu developer account: https://github.com/jasonacox/tinytuya/files/8145832/Tuya.IoT.API.Setup.pdf
#  This resulted in getting : Project ID : p1661694735485pkp3pc
#  Access ID/Client ID: u9vtjhsghvreq7kh34xa
# and Access Secret/Client Secret   fd365cf5fd444fae97e18a8771fe8bb9
# and 项目ID: p1661694735pkp3pc

# Then used the wizard to get access keys:

# Standard library imports
from time import sleep as time_sleep
from os import path
import datetime
from sys import exit as sys_exit
from subprocess import call

"""pi@RPi3-tankTemp:~/switch $ python3 -m tinytuya wizard 
TinyTuya Setup Wizard [1.6.6]

    Existing settings:
        API Key=x8dv4e847c3rjqnw8nh4 
        Secret=be4455ee9c3e4e56a26d34545a8cbec1
        DeviceID=bf5723e4b65de4a64fteqz
        Region=eu

    Use existing credentials (Y/n): n

    Enter API Key from tuya.com: u9vtjhsghvreq7kh34xa
    Enter API Secret from tuya.com: fd365cf5fd444fae97e18a8771fe8bb9
    Enter any Device ID currently registered in Tuya App (used to pull full list): bf5723e4b65de4a64fteqz

      Region List
        cn	China Data Center
        us	US - Western America Data Center
        us-e	US - Eastern America Data Center
        eu	Central Europe Data Center
        eu-w	Western Europe Data Center
        in	India Data Center

    Enter Your Region (Options: cn, us, us-e, eu, eu-w, or in): eu

>> Configuration Data Saved to tinytuya.json
{
    "apiKey": "u9vtjhsghvreq7kh34xa",
    "apiSecret": "fd365cf5fd444fae97e18a8771fe8bb9",
    "apiRegion": "eu",
    "apiDeviceID": "bf5723e4b65de4a64fteqz"
}


Device Listing

[
    {
        "name": "SWITCH03",
        "id": "bfae7fdb0b0c3c03522yoo",
        "key": "d196c29513b77291",
        "mac": "cc:8c:bf:57:27:c6"
    },
    {
        "name": "SWITCH02",
        "id": "bf0e00da7f4df8c38dxvqu",
        "key": "1a1a9ce5e6e6ebac",
        "mac": "cc:8c:bf:57:48:f1"
    },
    {
        "name": "SWITCH01",
        "id": "bf5723e4b65de4a64fteqz",
        "key": "4eb0c6992391377a",
        "mac": "cc:8c:bf:56:fa:b5"
    }
]



    # Example Usage of TinyTuya
import tinytuya
"""
        "name": "SWITCH01",
        "id": "bf5723e4b65de4a64fteqz",
        "key": "4eb0c6992391377a",
        "mac": "cc:8c:bf:56:fa:b5"
"""
d = tinytuya.OutletDevice('bf5723e4b65de4a64fteqz', '192.168.100.154', '4eb0c6992391377a')
d.set_version(3.3)
#data = d.status() 
#print('Device switch01  status: %r' % data)

nowait = True

#d.set_status(on, switch=1, nowait)
print("try on")
d.turn_on(switch=1, nowait=False)
print("done try on")
time_sleep(10)
print("try off")
#d.set_status(off, switch=1, nowait)
d.turn_on(switch=1, nowait=False)
print("done try off")


sys_exit()
time_sleep(3) 

"""
        "name": "SWITCH02",
        "id": "bf0e00da7f4df8c38dxvqu",
        "key": "1a1a9ce5e6e6ebac",
        "mac": "cc:8c:bf:57:48:f1
"""

d = tinytuya.OutletDevice('bf0e00da7f4df8c38dxvqu', '192.168.100.165', '1a1a9ce5e6e6ebac')
d.set_version(3.4)
data = d.status() 
print('Device switch02  status: %r' % data)

"""
        "name": "SWITCH03",
        "id": "bfae7fdb0b0c3c03522yoo",
        "key": "d196c29513b77291",
        "mac": "cc:8c:bf:57:27:c6
"""

d = tinytuya.OutletDevice('bfae7fdb0b0c3c03522yoo', '192.168.100.122', 'd196c29513b77291')
d.set_version(3.4)
data = d.status() 
print('Device switch03  status: %r' % data)
