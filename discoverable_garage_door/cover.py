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
from .button import Button
from .contact import Contact

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

contacts = {}
class Cover(Subscriber[CoverInfo]):
    """Implements an MQTT button:
    https://www.home-assistant.io/integrations/cover.mqtt
    """
    global contacts

    def __init__(cls, mqtt: Settings.MQTT, gpio_config: Config.GPIO, door_config: Config.GPIO.Door):
        cover_info = CoverInfo(name=door_config.name, device_class="garage")
        cover_settings = Settings(mqtt=mqtt, entity=cover_info)
        button = Button(door_config, gpio_config)
        opened_contact = Contact(door_config.opened_contact_pin, \
                gpio_config)
        opened_contact.addEventHandler(Cover.opened_contact_callback)
        closed_contact = Contact(door_config.closed_contact_pin, \
                gpio_config)
        closed_contact.addEventHandler(Cover.closed_contact_callback)
        super().__init__( \
                cover_settings, \
                command_callback=Cover.cover_callback, \
                user_data=button)
        cls.cover_info = cover_info
        cls.cover_settings = cover_settings
        cls.button = button
        cls.opened_contact = opened_contact
        cls.closed_contact = closed_contact
        cls.open()
        contacts[door_config.opened_contact_pin] = opened_contact
        contacts[door_config.closed_contact_pin] = closed_contact

    def open(cls):
        cls._send_action(state=cls._entity.payload_open)

    def close(cls):
        cls._send_action(state=cls._entity.payload_close)

    def stop(cls):
        cls._send_action(state=cls._entity.payload_stop)

    def _send_action(cls, state: str) -> None:
        if state in [
            cls._entity.payload_open,
            cls._entity.payload_close,
            cls._entity.payload_stop,
        ]:
            state_message = state
            logger.info(
                f"Sending {state_message} command to {cls._entity.name} using {cls.state_topic}"
            )
            cls._state_helper(state=state_message)

    def _update_state(cls, state) -> None:
        raise Error()

    def cleanup(cls):
        button.cleanup()
        opened_contact.cleanup()
        closed_contact.cleanup()

    @staticmethod
    def get_contact(pin:int) -> Contact:
        contact = contacts[pin]
        if contact != None:
            return contact
        raise Exception

    @staticmethod
    def opened_contact_callback(pin:int):
        contact = contacts[pin]
        logger.debug(f'opened contact pulsed: {contact}')
        state = contact.input()
        logger.debug(f'state: {state}')

    @staticmethod
    def closed_contact_callback(pin:int):
        contact = contacts[pin]
        logger.debug(f'closed contact pulsed: {contact}')
        state = contact.input()
        logger.debug(f'state: {state}')

    @staticmethod
    def cover_callback(client: Client, user_data, message: MQTTMessage):
        cover_payload = message.payload.decode()
        logging.info(f"Received {cover_payload} from HA with {user_data}")
        user_data.pushButtonFor()

    @staticmethod
    def cover(mqtt: Settings.MQTT, gpio_config: Config.GPIO, door_config: Config.GPIO.Door) -> Cover:
        return Cover(mqtt, gpio_config, door_config)
