
from hass_client import HomeAssistantClient


class Sensor:
    def __init__(self, hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """

        self._raw_sensor_info = sensor_info
        self._entity_id = sensor_info['entity_id']
        try:
            self._device_class = sensor_info['attributes']['device_class']
        except:
            self._device_class = ""
        self.friendly_name = sensor_info['attributes']['friendly_name']
        self.sensor_class = None
        self._hass_instance = hass_instance
        self._hass_instance.register_event_callback(self._process_hass_event)
        self._listeners = []
        self._event_callback = None

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

    async def _update_fields(self, event_details: dict) -> None:
        """
        | Updates the sensor data

        :param event_details: Event that triggered the update
        :type event_details: dict
        """
        #print("Update sensor")


    async def _process_hass_event(self, event: str, event_details: dict) -> None:

        """
        | Process events from homeassistant and filter them

        :param event: Type of event
        :type event: str

        :param event_details: Event data dictionary
        :type event_details: dict
        """
        if event == 'state_changed':
            if event_details['entity_id'] == self._entity_id:
                await self._update_fields(event_details)


    async def _on_event(self) -> None:
        """
        | Called when an event occurs
        | Must be awaited

        """
        if self._event_callback is not None:
            await self._event_callback(self)

    def set_event_callback(self, callback) -> None:
        """
        | Defines a callback to be called when the sensor changes its state

        :param callback: Function to be called
        :type callback: async fun
        """
        self._event_callback = callback