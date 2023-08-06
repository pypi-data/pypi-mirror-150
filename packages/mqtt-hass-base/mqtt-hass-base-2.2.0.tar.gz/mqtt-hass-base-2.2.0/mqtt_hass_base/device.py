"""MQTT Hass Base."""
import logging
from typing import Any, Dict, List, Optional, Union

import paho.mqtt.client as mqtt

from mqtt_hass_base import entity as mqtt_entity
from mqtt_hass_base.error import MQTTHassBaseError

ENTITY_TYPES = (
    "switch",
    "lock",
    "light",
    "binarysensor",
    "sensor",
    "vacuum",
)


class MqttDevice:
    """Mqtt device base class."""

    _entities: List[mqtt_entity.MqttEntity] = []

    def __init__(
        self,
        name: str,
        logger: logging.Logger,
        mqtt_discovery_root_topic: str,
        mqtt_data_root_topic: str,
    ):
        """Create a new device."""
        # Get logger
        self.logger = logger.getChild(name)
        self._name = name
        self.mqtt_discovery_root_topic = mqtt_discovery_root_topic
        self.mqtt_data_root_topic = mqtt_data_root_topic
        self._entities: List[mqtt_entity.MqttEntity] = []
        self._model: Optional[str] = None
        self._manufacturer: Optional[str] = None
        self._sw_version: Optional[str] = None
        self._via_device: Optional[str] = None
        self._identifiers: List[str] = []
        self._connections: List[List[str]] = []
        self._mac: Optional[str] = None

    def __repr__(self) -> str:
        """Get repr of the current device."""
        return f"<{self.__class__.__name__} '{self.name}'>"

    @property
    def entities(self) -> List[mqtt_entity.MqttEntity]:
        """Get the list of the entities of the devices."""
        return self._entities

    def add_entity(
        self,
        entity_type: "str",
        name: str,
        unique_id: str,
        entity_settings: dict[str, Any],
        subscriptions: Optional[dict[str, str]] = None,
        sub_mqtt_topic: Optional[str] = None,
    ) -> mqtt_entity.MqttEntity:
        """Add a new entity in the device."""
        if entity_type.lower() not in ENTITY_TYPES:
            msg = (
                f"Entity type '{entity_type}' is not supported. "
                f"Supported types are: {ENTITY_TYPES}"
            )
            self.logger.error(msg)
            raise MQTTHassBaseError(msg)

        if sub_mqtt_topic:
            mqtt_data_root_topic = "/".join(
                (self.mqtt_data_root_topic, sub_mqtt_topic.strip("/"))
            )
        else:
            mqtt_data_root_topic = self.mqtt_data_root_topic

        self.logger.info("Adding entity %s - %s", entity_type, name)
        ent = getattr(mqtt_entity, "Mqtt" + entity_type.capitalize())(
            name=name,
            unique_id=unique_id,
            mqtt_discovery_root_topic=self.mqtt_discovery_root_topic,
            mqtt_data_root_topic=mqtt_data_root_topic,
            logger=self.logger,
            device_payload=self.config_device_payload,
            subscriptions=subscriptions,
            **entity_settings,
        )
        self._entities.append(ent)
        return ent

    def set_mqtt_client(self, mqtt_client: mqtt.Client) -> None:
        """Set the mqtt client to each entity."""
        for entity in self.entities:
            entity.set_mqtt_client(mqtt_client)

    def register(self) -> None:
        """Register all entities in MQTT."""
        self.logger.info("Registering entities for device %s", self.name)
        for entity in self.entities:
            entity.register()

    def subscribe(self) -> None:
        """Subscribe to the MQTT topic needed for each entity."""
        self.logger.info("Subscribing to input mqtt topics")
        for entity in self.entities:
            entity.subscribe()

    def unregister(self) -> None:
        """Unregister all entities from MQTT."""
        self.logger.info("Unregistering entities for device %s", self.name)
        for entity in self.entities:
            entity.unregister()

    @property
    def name(self) -> Optional[str]:
        """Return the name of the device."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if name != self._name:
            self.logger = self.logger.getChild("device").getChild(name)
        self._name = name

    @property
    def model(self) -> Optional[str]:
        """Return the module of the device."""
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        self._model = model

    @property
    def manufacturer(self) -> Optional[str]:
        """Return the manufacturer of the device."""
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, manufacturer: str) -> None:
        self._manufacturer = manufacturer

    @property
    def sw_version(self) -> Optional[str]:
        """Return the software version of the device."""
        return self._sw_version

    @sw_version.setter
    def sw_version(self, sw_version: str) -> None:
        self._sw_version = sw_version

    @property
    def via_device(self) -> Optional[str]:
        """Return the intermediate device name of the current device."""
        return self._via_device

    @via_device.setter
    def via_device(self, via_device: str) -> None:
        self._via_device = via_device

    @property
    def identifiers(self) -> List[str]:
        """Return the identifiers of the device."""
        return self._identifiers

    @identifiers.setter
    def identifiers(self, id_: str) -> None:
        if id_ not in self._identifiers:
            self._identifiers.append(id_)

    @property
    def mac(self) -> Optional[str]:
        """Return the mac address of the device."""
        return self._mac

    @mac.setter
    def mac(self, value: str) -> None:
        self._mac = value
        self.connections = ["mac", value]  # type: ignore

    @property
    def connections(self) -> List[List[str]]:
        """Return the connection list of the device."""
        return self._connections

    @connections.setter
    def connections(self, raw_item: List[str]) -> None:
        try:
            item = list(raw_item)
        except TypeError as exp:
            self.logger.critical(f"Bad connection value: {raw_item}")
            raise MQTTHassBaseError from exp
        if len(item) != 2:
            raise MQTTHassBaseError(
                f"A connection need 2 elements but it's: {raw_item}"
            )
        if item not in self._connections:
            self._connections.append(item)

    @property
    def config_device_payload(self) -> dict[str, Any]:
        """Return the configuration device payload.

        This is the payload needed to register an entity of the current
        device in Home Assistant (using MQTT discovery).
        """
        payload: Dict[str, Union[Optional[str], List[str], List[List[str]]]] = {
            "name": self.name
        }
        if self.connections:
            payload["connections"] = self.connections
        if self.identifiers:
            payload["identifiers"] = self.identifiers
        if self.manufacturer:
            payload["manufacturer"] = self.manufacturer
        if self.model:
            payload["model"] = self.model
        if self.sw_version:
            payload["sw_version"] = self.sw_version
        if self.via_device:
            payload["via_device"] = self.via_device
        if "connections" not in payload and "identifiers" not in payload:
            msg = "You need to define identifiers or connections in the device attributes."
            self.logger.error(msg)
            raise MQTTHassBaseError(msg)
        return payload
