#! /usr/bin/python3

import os
import RNS
import LXMF
import time
from sbapp.sideband.sense import Telemeter
from sbapp.sideband.geo import euclidian_distance

delaytime = 1800
#ORD: 41.97983167658096, -87.90903385726247 668' ASL
basestation = [41.980,-87.909,203.6]
displayname = "Rangemapper - unconfigured"

def ReceiveTelemetry(lxm):
  print("Message Received")
  name = RNS.prettyhexrep(lxm.source_hash)
  print(name)
  if LXMF.FIELD_TELEMETRY not in lxm.fields:
    print("No telemetry found")
    return
  T = Telemeter.from_packed(lxm.fields[LXMF.FIELD_TELEMETRY])
  T = T.read_all()
  lat = T["location"]["latitude"]
  long = T["location"]["longtitude"]
  alt = T["location"]["altitude"]
  distance = euclidian_distance([lat,long,alt],basestation)
  print("Distance: "+str(distance))
  acc = T["location"]["accuracy"]
  messagetime = T["time"]["utc"]
  if lxm.rssi or lxm.snr:
    rssi = lxm.rssi
    snr = lxm.snr
    print("RSSI: "+str(rssi))
    print("SNR:  "+str(snr))

  buffer = str(name)+","+str(messagetime)+","+str(lat)+","+str(long)+","+str(alt)+","+str(acc)+","+str(distance)+","
  if rssi:
    buffer = buffer + str(rssi)
  buffer=buffer+","
  if snr:
    buffer = buffer+str(snr)
  print(buffer)
  if os.path.exists("RangeTelemetry.csv"):
    buffer = "\n"+buffer
  f = open("RangeTelemetry.csv","a")
  f.write(buffer)
  f.close()

R = RNS.Reticulum()
userdir = os.path.expanduser("~")
configdir = userdir+"/.nomadnetwork"
identitypath = configdir+"/storage/identity"
if os.path.exists(identitypath):
  ID = RNS.Identity.from_file(identitypath)
  print("Loading identity")
else:
  print("No identity found")
  sys.exit("Program uses NomadNet identity, please create one.")

L = LXMF.LXMRouter(identity = ID, storagepath = userdir+"/RangeMap")
L_dest = L.register_delivery_identity(ID,display_name = displayname)
L.register_delivery_callback(ReceiveTelemetry)

def MainLoop():
  global delaytime
  oldtime = 0
  print("Ready to receive")
  while True:
    newtime = time.time()
    if newtime > (oldtime + delaytime):
       oldtime = newtime
       L_dest.announce()
    time.sleep(1)

MainLoop()

print("END")

