from hass_client import HomeAssistantClient

from aiplusiot.sensors.standard_sensors.StandardSensor import StandardSensor
from aiplusiot.sensors.standard_sensors.SensorClasses import SensorClass


class PressureSensor(StandardSensor):
    def __init__(self,hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a Humidity sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """
        super().__init__(hass_instance,sensor_info)
        self.pressure = float(sensor_info['state'])
        self.sensor_class = SensorClass.PRESSURE

    def get_pressure(self) -> float:
        """
        | Gets the current humidity of the sensor


        :return: Current humidity
        :rtype: float
        """
        return self.pressure

    async def _update_fields(self, event_details: dict) -> None:
        await super(PressureSensor, self)._update_fields(event_details)

        self.pressure = float(event_details['new_state']['state'])
