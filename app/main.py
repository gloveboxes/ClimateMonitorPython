# Sample requires Python 3.7 or better

from azure.iot.device.aio import IoTHubDeviceClient
from device_provisioning_service import Device
from owm import Sensor
import asyncio
import json
import os
import sys


async def main():
    idScope = None
    deviceId = None
    derivedKey = None

    idScope = os.environ.get('idScope')
    deviceId = os.environ.get('deviceId')
    derivedKey = os.environ.get('derivedKey')
    owm_key = os.environ.get('owmKey')
    air_visual_key = os.environ.get('air_visual_key')

    if idScope is None or deviceId is None or derivedKey is None:
        sys.exit(1)

    dps = Device(idScope, deviceId, derivedKey)

    conn_str = await dps.connection_string

    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    await device_client.connect()

    sensor = Sensor(owm_key, air_visual_key)

    while True:
        try:
            telemetry = await sensor.get_weather()
            if telemetry is not None:

                print(telemetry)
                
                data = json.dumps(telemetry)

                await device_client.send_message(data)

                await asyncio.sleep(10)

        except:
            print("Unexpected error:", sys.exc_info()[0])

    await device_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
