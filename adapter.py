# adapter.py

"""
Adapter layer: polls Modbus TCP (PLC) and prints JSON payloads.
- Later add AES-GCM encryption and MQTT publishing. -
"""

import time
import json
import sys

from pymodbus.client import ModbusTcpClient

from config import *
MAX_RETRIES = 3
RETRY_DELAY = 3

if __name__ == "__main__":
    client = ModbusTcpClient(PLC_HOST, port=PLC_PORT)

    for attempt in range(1, MAX_RETRIES + 1):
        if not client.connect():
            if attempt < MAX_RETRIES:
                print(f"[Adapter] Attempt {attempt} Failed to connect to PLC at {PLC_HOST}:{PLC_PORT}")
                time.sleep(RETRY_DELAY)
            else:
                print(f"[Adapter] Used max attempts to connect to Modbus client: exiting...")
                sys.exit(1)

    print(f"[Adapter] Connected to PLC at {PLC_HOST}:{PLC_PORT}")

    try:
        while True:
            rr = client.read_holding_registers(TEMP_REGISTER, count=1, device_id=1)
            if rr.isError():
                print(f"[Adapter] failed to read register")
            else:
                temp = rr.registers[0]
                payload = {
                    "device": "temperature_plc",
                    "temperature": temp,
                    "unit": "F",
                    "timestamp": time.time()
                }
                print("[Adapter] JSON payload:", json.dumps(payload))

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Adapter] Shutting down.")
    finally:
        client.close()