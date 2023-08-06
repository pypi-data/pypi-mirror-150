from hass_client import HomeAssistantClient

from aiplusiot.sensors.Sensor import Sensor


class StandardSensor(Sensor):
    def __init__(self, hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """
        super().__init__(hass_instance, sensor_info)
        try:
            self.state_class = sensor_info['attributes']['state_class']
        except Exception as e:
            print('Sensor without state class: '+ self.friendly_name)

        self.unit_of_measurement = sensor_info['attributes']['unit_of_measurement']

    async def _update_fields(self, event_details: dict) -> None:
        await super(StandardSensor, self)._update_fields(event_details)

        await self._on_event()
