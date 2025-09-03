# plc_device.py

"""
Simulated PLC device exposing temperature data via Modbus TCP.

- Uses pymodbus to HOST a Modbus server.
- Temperature is a function of time of day (sinusoidal) with noise.
- Adapter.py will poll this register to get readings.
"""

import asyncio
import math
import random
import datetime as dt

from pymodbus.datastore import ModbusDeviceContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer

# Get tcp settings
from config import *


def gen_temp():
    """Generate a temperature given time of day plus noise"""
    now = dt.datetime.now()
    seconds = now.hour * 3600 + now.minute * 60 + now.second

    # 24hr sycle as a sin wave between 50 and 100 degrees
    base = 75 + 25 * math.sin(2 * math.pi * seconds / 86400)
    noise = random.uniform(-1, 1)
    return int(base + noise)

async def update_registers(device):
    """Periodically update Modbus registers with new temperature values"""
    while True:
        temp = gen_temp()
        device.setValues(3, 0, [temp])
        print(f"[PLC-Temperature] Updated temperature register to {temp} °F")
        await asyncio.sleep(1)

async def run_server():
    """Sets up the Modbus datastore (device context)"""
    # Create a simple data block with 100 holding registers
    store = ModbusSequentialDataBlock(0, [0] * 100)
    device = ModbusDeviceContext(hr=store)
    context = ModbusServerContext(devices={1: device}, single=False)

    # Start background task to update registers
    asyncio.create_task(update_registers(device))

    # Start Modbus TCP server
    print(f"[PLC-Temperature] Starting Modbus server on {PLC_HOST}:{PLC_PORT}")
    await StartAsyncTcpServer(context=context, address=(PLC_HOST, PLC_PORT))


if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\n[PLC-Temperature] Shutting down.")