from hass_client import HomeAssistantClient

from aiplusiot.sensors.standard_sensors.StandardSensor import StandardSensor
from aiplusiot.sensors.standard_sensors.SensorClasses import SensorClass


class IlluminanceSensor(StandardSensor):
    def __init__(self,hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a Illuminance sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """
        super().__init__(hass_instance, sensor_info)
        self.sensor_class = SensorClass.ILLUMINANCE
        self.luminance = sensor_info['state']

    def get_illuminance(self) -> int:
        """
        | Gets the current illuminance on the sensor


        :return: Current illuminance
        :rtype: int
        """
        return self.luminance

    async def _update_fields(self, event_details: dict) -> None:
        await super(IlluminanceSensor, self)._update_fields(event_details)

        self.luminance = event_details['new_state']['state']