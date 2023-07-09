from __future__ import annotations
import logging
import logging.config
from typing import Optional
from .util import logger

from ha_mqtt_discoverable import (
    DeviceInfo,
    Discoverable,
    EntityInfo,
    Subscriber,
    Settings,
)
from .config import Config

"""
# Example configuration.yaml entry
mqtt:
  button:
    - unique_id: bedroom_switch_reboot_btn
      name: "Restart Bedroom Switch"
      command_topic: "home/bedroom/switch1/commands"
      payload_press: "restart"
      availability:
        - topic: "home/bedroom/switch1/available"
      qos: 0
      retain: false
      entity_category: "config"
      device_class: "restart"
"""


class CoverInfo(EntityInfo):
    """Specific information for cover"""

    component: str = "cover"
    enabled_by_default: Optional[bool] = True
    name: str = "My Garage Door"
    object_id: Optional[str] = "my-garage-door-"
    unique_id: Optional[str] = "abc-cba"
    device_class: Optional[str] = "garage"

    payload_open: str = "open"
    """The payload to send to trigger the open action."""
    payload_close: Optional[str] = None
    """The payload to send to trigger the close action."""
    payload_stop: str = "stop"
    """The payload to send to trigger the stop action."""
    payload_opening: str = "opening"
    """The the opening state."""
    payload_closed: str = "closed"
    """The the closing state."""
    payload_closing: str = "closing"
    """The the closing state."""
    retain: Optional[bool] = None
    """If the published message should have the retain flag on or not"""


class Cover(Subscriber[CoverInfo]):
    """Implements an MQTT button:
    https://www.home-assistant.io/integrations/cover.mqtt
    """

    def open(self):
        self._send_action(state=self._entity.payload_open)

    def close(self):
        self._send_action(state=self._entity.payload_close)

    def stop(self):
        self._send_action(state=self._entity.payload_stop)

    def _send_action(self, state: str) -> None:
        if state in [
            self._entity.payload_open,
            self._entity.payload_close,
            self._entity.payload_stop,
        ]:
            state_message = state
            logger.info(
                f"Sending {state_message} command to {self._entity.name} using {self.state_topic}"
            )
            self._state_helper(state=state_message)

    def _update_state(self, state) -> None:
        raise Error()

    def cover_callback(client: Client, user_data, message: MQTTMessage):
        cover_payload = message.payload.decode()
        logging.info(f"Received {cover_payload} from HA")

    @staticmethod
    def cover(
        mqtt: Settings.MQTT, gpio_config: Config.GPIO, door_config: Config.GPIO.Door
    ) -> Cover:
        cover_info = CoverInfo(name=door_config.name, device_class="garage")
        cover_settings = Settings(mqtt=mqtt, entity=cover_info)
        cover = Cover(cover_settings, command_callback=Cover.cover_callback)
        cover.open()
        return cover
