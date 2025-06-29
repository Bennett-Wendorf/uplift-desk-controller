import asyncio
import time
import sys
from bleak import BleakScanner, BleakClient
from bleak.uuids import normalize_uuid_16
from bleak.backends.device import BLEDevice
from bleak.backends.bluezdbus.service import BleakGATTServiceBlueZDBus
from bleak.backends.bluezdbus.characteristic import BleakGATTCharacteristicBlueZDBus
from bleak.backends.bluezdbus.descriptor import BleakGATTDescriptorBlueZDBus

from uplift import Desk, discover

primary_service_uuid_for_discovery  = normalize_uuid_16(0xfe60)

timeout = 10.0

def print_command_options():
    print("Commands:")
    print("    h - print this help message")
    print("    u - move_to_standing")
    print("    d - move_to_sitting")
    print("    r - press_raise")
    print("    l - press_lower")
    print("    e - exit")
    print("    v - dump debug info")

def get_gatt_service_string(service: BleakGATTServiceBlueZDBus) -> str:
    return f"{service.uuid} - {service.description}"

async def get_gatt_characteristic_string(characteristic: BleakGATTCharacteristicBlueZDBus, bleak_client: BleakClient) -> str:
    value: str = await bleak_client.read_gatt_char(characteristic.uuid)
    return f"{characteristic.uuid} - {characteristic.description} - ({', '.join(characteristic.properties)}): {value}"

def get_gatt_descriptor_string(descriptor: BleakGATTDescriptorBlueZDBus) -> str:
    return f"{descriptor.uuid} - {descriptor.description}"

async def dump_client_info(bleak_client: BleakClient):
    print(f"Address: {bleak_client.address}")

    print("Services:")
    for service in bleak_client.services.services.values():
        print(f"\t{get_gatt_service_string(service)}")
        for characteristic in service.characteristics:
            print(f"\t\t{await get_gatt_characteristic_string(characteristic, bleak_client)}")
            for descriptor in characteristic.descriptors:
                print(f"\t\t\t{get_gatt_descriptor_string(descriptor)}")

async def async_height_notify_callback(desk: Desk):
    print(f"Received height update: {desk.height}; Moving: {desk.moving}")

async def main():
    desks: list[BLEDevice] = await discover()
    if len(desks) == 0:
        print("No desks found")
        return
    print(f"Found {len(desks)} desk(s)")
    for desk in desks:
        print(f"    - {desk.name} - {desk.address}")       

    first_desk = desks[0]
    print(f"Connecting to {first_desk.name} - {first_desk.address}...")

    async with BleakClient(first_desk) as bleak_client:
        print(f"Connected to {bleak_client.address}")
        
        desk = Desk(first_desk.address, first_desk.name, bleak_client)

        desk.register_callback(async_height_notify_callback)

#        await desk.start_notify()
#        await desk.read_height(bleak_client)
        print(f"Height: {desk.height} in")
        
        print("Start typing and press ENTER...\n Press h for help")

        loop = asyncio.get_running_loop()

        while True:
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)

            # data will be empty on EOF (e.g. CTRL+D on *nix)
            if not data:
                break

            if (data == b"u\n"):
                print("move_to_standing")
                await desk.move_to_standing()
            elif (data == b"d\n"):
                print("move_to_sitting")
                await desk.move_to_sitting()
            elif (data == b"r\n"):
                print("press_raise")
                await desk.press_raise()
            elif (data == b"l\n"):
                print("press_lower")
                await desk.press_lower()
            elif (data == b"h\n"):
                print_command_options()
            elif (data == b"e\n"):
                print("exit")
                break
            elif (data == b"v\n"):
                await dump_client_info(bleak_client)
            else:
                print("Unknown command")
                print_command_options()

#        await desk.stop_notify()
        print(f"Height: {desk.height} in")

if __name__ == "__main__":
    asyncio.run(main())
