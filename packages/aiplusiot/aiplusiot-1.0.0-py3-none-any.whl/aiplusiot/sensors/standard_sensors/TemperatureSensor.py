from hass_client import HomeAssistantClient

from aiplusiot.sensors.standard_sensors.StandardSensor import StandardSensor
from aiplusiot.sensors.standard_sensors.SensorClasses import SensorClass


class TemperatureSensor(StandardSensor):
    def __init__(self,hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a Temperature sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """
        super().__init__(hass_instance,sensor_info)
        self.temperature = float(sensor_info['state'])
        self.sensor_class = SensorClass.TEMPERATURE

    def get_temperature(self) -> float:
        """
        | Gets the current temperature on the sensor


        :return: Current temperature
        :rtype: float
        """
        return self.temperature

    async def _update_fields(self, event_details: dict) -> None:
        await super(TemperatureSensor, self)._update_fields(event_details)

        self.temperature = float(event_details['new_state']['state'])

