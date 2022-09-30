# from asyncio import get_event_loop
# from mqttsn.transports import UDP_MQTTSN_Transport

# async def main():
#     get_event_loop().create_datagram_endpoint(UDP_MQTTSN_Transport, None, ("broker", ))

# loop = get_event_loop()
# loop.run_until_complete(main())
# loop.close()

import asyncio
import serial_asyncio
from mqttsn.transports import XBEE_MQTTSN_Transport

loop = asyncio.get_event_loop()

loop.run_until_complete(
    serial_asyncio.create_serial_connection(
        loop,
        XBEE_MQTTSN_Transport,
        "/dev/ttyUSB0",
        baudrate=115200,
    ))
loop.run_forever()
loop.close()