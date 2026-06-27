"""Top level package for uplift-desk"""

from __future__ import annotations

__author__ = """Bennett Wendorf"""
___email___ = """bennett@bennettwendorf.dev"""

from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic
from bleak.exc import BleakDBusError
from bleak.uuids import normalize_uuid_16
from bleak.backends.device import BLEDevice
from typing import Self
import time

from .utils import height_conv_to_in

# Known GATT layouts across Jiecang-based desk variants.
# Each entry: (service, control/write characteristic, height/notify characteristic)
_KNOWN_LAYOUTS = [
    (normalize_uuid_16(0xfe60), normalize_uuid_16(0xfe61), normalize_uuid_16(0xfe62)),
    (normalize_uuid_16(0xff00), normalize_uuid_16(0xff01), normalize_uuid_16(0xff02)),
]

# Advertise/discover on all known primary services.
_primary_service_uuids_for_discovery = [layout[0] for layout in _KNOWN_LAYOUTS]

# Defaults preserve original behavior until a connected client tells us otherwise.
_desk_control_uuid = _KNOWN_LAYOUTS[0][1]
_desk_height_uuid = _KNOWN_LAYOUTS[0][2]

_wake_uuid = [0xf1, 0xf1, 0x00, 0x00, 0x00, 0x7e] # The content of this command actually doesn't seem to matter, the desk just needs to wake up
_sit_preset_uuid = [0xf1, 0xf1, 0x05, 0x00, 0x05, 0x7e]
_stand_preset_uuid = [0xf1, 0xf1, 0x06, 0x00, 0x06, 0x7e]
_raise_button_uuid = [0xf1, 0xf1, 0x01, 0x00, 0x01, 0x7e]
_lower_button_uuid = [0xf1, 0xf1, 0x02, 0x00, 0x02, 0x7e]
_status_uuid = [0xf1, 0xf1, 0x07, 0x00, 0x07, 0x7e]

_scanner_timeout = 10.0

def discover(scanner: BleakScanner = None) -> list[BLEDevice]:
    if scanner is None:
        scanner = BleakScanner()

    return scanner.discover(timeout=_scanner_timeout, service_uuids=_primary_service_uuids_for_discovery)

class Desk:
    def __init__(self, address: str, name: str, bleak_client: BleakClient = None) -> Self:
        self.address = address
        self.name = name
        self._height: float = 0.0
        self.bleak_client = bleak_client
        self._moving = False
        self._last_heights = []
        self._height_notification_callbacks: list[callable] = []
        self._resolved_uuids: tuple[str, str] | None = None

    @property
    def height(self):
        return self._height

    @property
    def moving(self):
        return self._moving

    def _set_moving(self, value: bool):
        self._moving = value
        self._last_action_time = time.time()

    def _resolve_uuids(self, client: BleakClient) -> tuple[str, str]:
        """Pick the (control, height) UUIDs matching the layout this desk exposes."""
        if self._resolved_uuids is not None:
            return self._resolved_uuids

        present = {s.uuid.lower() for s in client.services}
        for service_uuid, control_uuid, height_uuid in _KNOWN_LAYOUTS:
            if service_uuid.lower() in present:
                self._resolved_uuids = (control_uuid, height_uuid)
                return self._resolved_uuids

        # Fall back to the original defaults if nothing matched.
        self._resolved_uuids = (_desk_control_uuid, _desk_height_uuid)
        return self._resolved_uuids

    async def move_to_standing(self, bleak_client: BleakClient = None) -> None:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        await self._awaken(client)
        control_uuid, _ = self._resolve_uuids(client)
        await client.write_gatt_char(control_uuid, _stand_preset_uuid, False)

    async def move_to_sitting(self, bleak_client: BleakClient = None) -> None:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        await self._awaken(client)
        control_uuid, _ = self._resolve_uuids(client)
        await client.write_gatt_char(control_uuid, _sit_preset_uuid, False)

    async def press_raise(self, bleak_client: BleakClient = None) -> None:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        await self._awaken(client)
        control_uuid, _ = self._resolve_uuids(client)
        await client.write_gatt_char(control_uuid, _raise_button_uuid, False)

    async def press_lower(self, bleak_client: BleakClient = None) -> None:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        await self._awaken(client)
        control_uuid, _ = self._resolve_uuids(client)
        await client.write_gatt_char(control_uuid, _lower_button_uuid, False)

    async def start_notify(self, bleak_client: BleakClient = None) -> None:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        _, height_uuid = self._resolve_uuids(client)
        await client.start_notify(height_uuid, self._height_notify_callback)

    async def stop_notify(self, bleak_client: BleakClient = None) -> None:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        _, height_uuid = self._resolve_uuids(client)
        try:
            await client.stop_notify(height_uuid)
        except BleakDBusError:
            pass

    async def read_height(self, bleak_client: BleakClient = None) -> float:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        self._last_action_time = time.time()
        control_uuid, height_uuid = self._resolve_uuids(client)
        await client.write_gatt_char(control_uuid, _status_uuid, False)
        self._height = height_conv_to_in(await client.read_gatt_char(height_uuid))
        return self.height

    def register_callback(self, callback: callable) -> None:
        self._height_notification_callbacks.append(callback)

    def deregister_callback(self, callback: callable) -> None:
        self._height_notification_callbacks.remove(callback)

    def __str__(self):
        return f"{self.name} - {self.address}"

    async def _height_notify_callback(self, sender: BleakGATTCharacteristic, data: bytearray):
        self._height = height_conv_to_in(data)

        if (len(self._last_heights) > 0 and self._last_heights[-1] != self._height):
            self._set_moving(True)

        self._last_heights.append(self._height)
        if len(self._last_heights) > 4:
            if (self.moving
                and self._last_action_time + 1 < time.time() # Only set moving to false if we've been moving for more than 1 second (sometimes the first few height updates are the same)
                and self._last_heights[0] == self._height 
                and self._last_heights[1] == self._height
                and self._last_heights[2] == self._height
                and self._last_heights[3] == self._height):
                self._set_moving(False)

            self._last_heights.pop(0)
        
        for callback in self._height_notification_callbacks:
            await callback(self)

    async def _awaken(self, bleak_client: BleakClient = None) -> None:
        client = bleak_client or self.bleak_client

        if (client is None):
            raise Exception("No bleak client provided")

        control_uuid, _ = self._resolve_uuids(client)
        await client.write_gatt_char(control_uuid, _wake_uuid, False)
