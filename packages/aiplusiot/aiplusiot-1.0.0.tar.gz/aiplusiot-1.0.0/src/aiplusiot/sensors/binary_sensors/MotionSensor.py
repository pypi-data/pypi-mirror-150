from aiplusiot.sensors.binary_sensors.BinarySensor import BinarySensor
from hass_client import HomeAssistantClient

from aiplusiot.sensors.Sensor import Sensor
from aiplusiot.sensors.binary_sensors.BinarySensorClasses import BinarySensorClass


class MotionSensor(BinarySensor):
    def __init__(self, hass_instance: HomeAssistantClient, sensor_info: dict) -> None:
        """
        | Initializes a Motion sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """
        super().__init__(hass_instance, sensor_info)
        self.sensor_class = BinarySensorClass.MOTION

    async def _update_fields(self, event_details: dict) -> None:
        await super(MotionSensor, self)._update_fields(event_details)
        print('MOTION')
