from paho.mqtt import client as mqtt
import ssl
import json

# edge device root certificate 
path_to_root_cert = "./edge-device-ca-root.cert.pem"
# iot device name
device_id = "jcotest"
# sas token : can be generated with iothub-explorer sas-token <device-id>
sas_token = "SharedAccessSignature sr=jcohub.azure-devices.net%2Fdevices%2Fjcotest&sig=H2GUaY0J4ABnp%2F6NYG4bbd13U3bJzmFjuOn33K1cWMU%3D&se=1522313011"
# name of the iot hub
iot_hub_name = "jcohub"
# name of the IoT Edge Gateway
gateway_hostname = "desktop-vj6e6gs.localdomain"

def on_connect(client, userdata, flags, rc):
  print ("Device connected with result code: " + str(rc))

def on_disconnect(client, userdata, rc):
  print ("Device disconnected with result code: " + str(rc))

def on_publish(client, userdata, mid):
  print ("Device sent message")

client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.username_pw_set(username= iot_hub_name + ".azure-devices.net/" + device_id + "/api-version=2016-11-14", password=sas_token)

client.tls_set(ca_certs=path_to_root_cert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
client.tls_insecure_set(False)

client.connect(gateway_hostname, port=8883)

jsonPayload = {
  "id":123
}

payloadAsStr = str(jsonPayload)
print ( payloadAsStr )

client.publish("devices/" + device_id + "/messages/events/", json.dumps(jsonPayload), qos=1)
client.loop_forever()