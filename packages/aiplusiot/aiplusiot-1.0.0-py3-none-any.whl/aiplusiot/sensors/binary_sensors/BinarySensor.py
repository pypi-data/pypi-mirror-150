from hass_client import HomeAssistantClient

from aiplusiot.sensors.Sensor import Sensor


class BinarySensor(Sensor):
    def __init__(self, hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a Binary sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """
        super().__init__(hass_instance, sensor_info)

        self.string_state = sensor_info['state']
        if self.string_state == 'on':
            self.bool_state = True
        else:
            self.bool_state = False

    def get_entity_id(self) -> str:
        """
        | Gets the entity id of the sensor


        :return: Entity id
        :rtype: str
        """
        return self._entity_id

    def get_name(self) -> str:
        """
        | Gets the entity id of the sensor


        :return: Entity id
        :rtype: str
        """
        return self.friendly_name

    def get_state(self) -> bool:

        """
        | Process events from homeassistant and filter them

        :param event: Type of event
        :type event: str

        :param event_details: Event data dictionary
        :type event_details: dict
        """
        return self.bool_state

    async def _update_fields(self, event_details: dict) -> None:
        await super(BinarySensor, self)._update_fields(event_details)
        self.string_state = event_details['new_state']['state']
        if self.string_state == 'on':
            self.bool_state = True
        else:
            self.bool_state = False

        await self._on_event()
