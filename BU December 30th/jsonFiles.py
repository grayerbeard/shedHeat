# Python program to read
# json file
  
  
import json
  
# Opening JSON file
f = open('devices.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
deviceName = "SWITCH01"
print("Device  : ",deviceName, "  id is: ",data["name" == deviceName]["id"])
  
# Closing file
f.close()

# Opening JSON file
f = open('tinytuya.json')
data = json.load(f)
print("apiKey is: ",data["apiKey"])
print("apiSecret is: ",data["apiSecret"])
print("apiRegion: ",data["apiRegion"])
print("apiDeviceID is: ",data["apiDeviceID"])
