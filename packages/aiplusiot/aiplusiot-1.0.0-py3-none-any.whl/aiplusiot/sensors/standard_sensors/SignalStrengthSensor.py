from hass_client import HomeAssistantClient

from aiplusiot.sensors.standard_sensors.StandardSensor import StandardSensor
from aiplusiot.sensors.standard_sensors.SensorClasses import SensorClass


class SignalStrengthSensor(StandardSensor):
    def __init__(self,hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a Signal Strength sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """
        super().__init__(hass_instance, sensor_info)
        self.sensor_class = SensorClass.SIGNAL_STRENGTH
        self.signal_strength = sensor_info['state']

    def get_signal_strength(self) -> int:
        """
        | Gets the current illuminance on the sensor


        :return: Current signal strength
        :rtype: int
        """
        return self.signal_strength

    async def _update_fields(self, event_details: dict) -> None:
        await super(SignalStrengthSensor, self)._update_fields(event_details)

        self.signal_strength = event_details['new_state']['state']