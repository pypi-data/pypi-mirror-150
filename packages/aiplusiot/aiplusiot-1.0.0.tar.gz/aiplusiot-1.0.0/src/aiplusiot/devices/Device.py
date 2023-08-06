from aiplusiot.actuators.Light import Light
from aiplusiot.sensors.binary_sensors import BinarySensor
from aiplusiot.sensors.standard_sensors import StandardSensor
from aiplusiot.switches import Switch


class Device:
    def __init__(self, device_info_dict):
        self.device_id = device_info_dict['id']
        self.manufacturer = device_info_dict['manufacturer']
        self.model = device_info_dict['model']
        self.user_defined_name = device_info_dict['name_by_user']
        self.name = device_info_dict['name']
        self._standard_sensors = []
        self._switches = []
        self._lights = []
        self._binary_sensors = []

    def add_standard_sensor(self, sensor: StandardSensor) -> None:
        self._standard_sensors.append(sensor)

    def add_binary_sensor(self, sensor: BinarySensor) -> None:
        self._binary_sensors.append(sensor)

    def add_light(self,light: Light) -> None:
        self._lights.append(light)

    def add_switch(self, switch: Switch) -> [Switch]:
        return self._switches.append(switch)

    def get_standard_sensors(self) -> [StandardSensor]:
        return self._standard_sensors

    def get_binary_sensors(self) -> [BinarySensor]:
        return self._binary_sensors

    def get_lights(self) -> [Light]:
        return self._lights

    def get_switches(self) -> [Switch]:
        return self._switches

    def is_empty(self) -> bool:
        return len(self._standard_sensors)+len(self._switches)+len(self._lights)+len(self._binary_sensors) == 0
