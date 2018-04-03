# Azure IoT Edge - Python MQTT

## Description

This repository provides code samples that demonstrate how to use pure MQTT in Python (using paho-mqtt) to send message to Azure IoT Edge Hub.

## MQTT Simulator

This is a simple Python application that sends a message to an MQTT endpoint every 10 seconds.

### Usage

```bash
cd src/mqtt-simulator
pip install -r requirements.txt
chmod +x main.py
./main.py -c <certPath> -d <deviceId> -n <hubName> -g <gatewayHostname> -t <sasToken>
```

Where:

- `certPath` is the path to the Edge device root certificate
- `deviceId` is the id of the Azure IoT Edge device
- `hubName` is the name of the Azure IoT Hub
- `gatewayHostname` is the hostname of the Azure IoT Edge gateway
- `sasToken` is the shared access token that will be use to authenticate through Azure IoT Hub. It can be generated using `iothub-explorer sas-token DEVICE_ID`

## Azure IoT Edge Deployment

The `deployment.json` file located in the `src` folder contains a simple deployment definition that can be applied to an Azure IoT Edge device. It only deploy the `edgeAgent`, the `edgeHub` and a simple route that sends all messages from the Edge Hub to Azure IoT Hub ($upstream):

```json
"routes": {
    "route": "FROM /* INTO $upstream"
}
```

## Check Azure IoT Edge Hub logs

You can check the messages are received by the Azure IoT Edge Hub using the following command on the gateway:

```bash
docker logs -f edgeHub
```

## Monitor Azure IoT Hub messages

You can monitor messages sent to Azure IoT Hub using the [iothub-explorer tool](https://github.com/azure/iothub-explorer) or Visual Studio Code with the [Azure IoT Extentions](https://marketplace.visualstudio.com/items?itemName=vsciot-vscode.azure-iot-edge).