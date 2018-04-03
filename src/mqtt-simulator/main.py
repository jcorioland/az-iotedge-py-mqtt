#!/usr/bin/python

from paho.mqtt import client as mqtt
import ssl
import json
import sys
import getopt
import time

def usage():
  print ("Usage: ./main.py -c <certPath> -d <deviceId> -n <hubName> -g <gatewayHostname> -t <sasToken>")

def on_connect(client, userdata, flags, rc):
  print ("Device connected with result code: " + str(rc))

def on_disconnect(client, userdata, rc):
  print ("Device disconnected with result code: " + str(rc))

def on_publish(client, userdata, mid):
  print ("Device sent message")

def main(argv):
  certPath = ''
  deviceId = ''
  hubName = ''
  gatewayHostname = ''
  sasToken = ''
  try:
    opts, args = getopt.getopt(argv, 'c:d:n:g:t:h', ['cert-path=','device-id=','hub-name=', 'gateway-hostname=', 'sas-token=', 'help'])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      usage()
      sys.exit()
    elif opt in ('-c', '--cert-path'):
      certPath = arg
    elif opt in ('-d', '--device-id'):
      deviceId = arg
    elif opt in ('-n', '--hub-name'):
      hubName = arg
    elif opt in ('-g', '--gateway-hostname'):
      gatewayHostname = arg
    elif opt in ('-t', '--sas-token'):
      sasToken = arg
  if certPath == '' or deviceId == '' or hubName == '' or gatewayHostname == '' or sasToken == '':
    usage()
    sys.exit(2)
  else:
    try:
      client = mqtt.Client(client_id=deviceId, protocol=mqtt.MQTTv311)
      client.on_connect = on_connect
      client.on_disconnect = on_disconnect
      client.on_publish = on_publish
      client.username_pw_set(username= hubName + ".azure-devices.net/" + deviceId + "/api-version=2016-11-14", password=sasToken)
      client.tls_set(ca_certs=certPath, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
      client.tls_insecure_set(False)
      client.connect(gatewayHostname, port=8883)
      while True:
        client.publish("devices/" + deviceId + "/messages/events/", "hello mqtt", qos=1)
        client.loop()
        time.sleep(2)
    except Exception as e:
      print ("An error has occured: %s" % e)
    client.disconnect()

if __name__ == "__main__":
  main(sys.argv[1:])