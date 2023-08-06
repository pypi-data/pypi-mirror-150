import asyncio
from typing import Dict, Any

from aiplusiot.devices.Device import Device
from aiplusiot.image_processors.ImageProcessor import ImageProcessor
from aiplusiot.sensors.binary_sensors.SoundSensor import SoundSensor
from aiplusiot.sensors.standard_sensors.CO2Sensor import CO2Sensor
from aiplusiot.sensors.standard_sensors.CurrentSensor import CurrentSensor
from aiplusiot.sensors.standard_sensors.NoiseSensor import NoiseSensor
from aiplusiot.sensors.standard_sensors.PressureSensor import PressureSensor
from hass_client import HomeAssistantClient

from aiplusiot.actuators.Light import Light
from aiplusiot.sensors.Sensor import Sensor
from aiplusiot.sensors.binary_sensors.HeatSensor import HeatSensor
from aiplusiot.sensors.binary_sensors.IasZoneSensor import IasZoneSensor
from aiplusiot.sensors.binary_sensors.MotionSensor import MotionSensor
from aiplusiot.sensors.binary_sensors.OccupancySensor import OccupancySensor
from aiplusiot.sensors.binary_sensors.OpeningSensor import OpeningSensor
from aiplusiot.sensors.binary_sensors.ProblemSensor import ProblemSensor
from aiplusiot.sensors.standard_sensors import StandardSensor
from aiplusiot.sensors.standard_sensors.BatterySensor import BatterySensor
from aiplusiot.sensors.standard_sensors.HumiditySensor import HumiditySensor
from aiplusiot.sensors.standard_sensors.IlluminanceSensor import IlluminanceSensor
from aiplusiot.sensors.standard_sensors.ObjectsSensor import ObjectsSensor
from aiplusiot.sensors.standard_sensors.SensorClasses import SensorClass
from aiplusiot.sensors.binary_sensors.BinarySensorClasses import BinarySensorClass
import logging

from aiplusiot.sensors.binary_sensors.BinarySensor import BinarySensor

# LOGGER = logging.getLogger()
from aiplusiot.sensors.standard_sensors.SignalStrengthSensor import SignalStrengthSensor
from aiplusiot.sensors.standard_sensors.TemperatureSensor import TemperatureSensor
from aiplusiot.switches.Switch import Switch


class AiPlusIOT:
    _lights: [Light]

    def __init__(self, url, token):
        """
        | Creates a IOTLib instance to connect to HomeAssistant

        :param url: Adress of the HomeAssistant server
        :type url: str
        :param token: Long lived access token
        :type token: str
        """
        self._url = url
        self._token = token
        self._hass_instance = HomeAssistantClient(self._url, self._token)
        self._hass_instance.register_event_callback(self._manage_hass_event)
        self._sensors = {}
        self._binary_sensors = {}
        self._devices = {}
        self._lights = []
        self._switches = []
        self._image_processors = []

    def _initialize_sensors(self):
        """
        | Initializes the sensors present in the homeassistant instance
        """
        for sensor in self._hass_instance.sensors:
            # print("Sensor: %s", str(sensor))
            s = None
            if sensor['entity_id'].startswith("sensor.browser"):
                pass
            else:
                try:
                    if sensor['attributes']['device_class'] in self._sensors.keys():
                        s = self._create_sensor(sensor)
                        self._sensors[sensor['attributes']['device_class']].append(s)
                    else:
                        s = self._create_sensor(sensor)

                        self._sensors[sensor['attributes']['device_class']] = [s]
                except Exception as e:
                    try:
                        print("Sensor without device class " + sensor['attributes']['friendly_name'])
                        if sensor['attributes']['unit_of_measurement'] == 'objects':
                            s = ObjectsSensor(self._hass_instance, sensor)
                            self._sensors['objects'] = [s]
                        if sensor['attributes']['unit_of_measurement'] == 'dB':
                            s = NoiseSensor(self._hass_instance, sensor)
                            self._sensors['objects'] = [s]
                    except Exception as e:
                        print("Could not add sensor " + str(sensor))
                if s is not None:
                    self._devices[self._hass_instance.entity_registry[s._entity_id]['device_id']].add_standard_sensor(s)

    def _initialize_binary_sensors(self):
        """
        | Initializes the binary sensors present in the homeassistant instance
        """
        for sensor in self._hass_instance.binary_sensors:
            # LOGGER.info("Sensor: %s",str(sensor))
            s = None
            try:
                if sensor['attributes']['device_class'] in self._binary_sensors.keys():
                    s = self._create_binary_sensor(sensor)
                    self._binary_sensors[sensor['attributes']['device_class']].append(s)
                else:
                    s = self._create_binary_sensor(sensor)

                    self._binary_sensors[sensor['attributes']['device_class']] = [s]
            except Exception as e:
                print(e)
                print("Could not add sensor " + str(sensor))
            if s is not None:
                try:
                    self._devices[self._hass_instance.entity_registry[s._entity_id]['device_id']].add_binary_sensor(s)
                except Exception as e:
                    print('Device not found for ' + str(s))

    def _initialize_switches(self):
        """
        | Initializes tha switches present in the homeassistant instance
        """
        for switch in self._hass_instance.switches:
            s = Switch(self._hass_instance, switch)
            self._switches.append(s)

            self._devices[self._hass_instance.entity_registry[s._entity_id]['device_id']].add_switch(s)

    def _initialize_lights(self):
        """
        | Initializes the lights present at the homeassistant instance
        """
        for light in self._hass_instance.lights:
            if not light['entity_id'].startswith('light.browser_'):
                l = Light(self._hass_instance, light)
                self._lights.append(l)
                print('Added light', l)

                self._devices[self._hass_instance.entity_registry[l._entity_id]['device_id']].add_light(l)
    def _initialize_image_processors(self):
        for state in self._hass_instance.states:
            if state.startswith('image_processing'):
                self._image_processors.append(ImageProcessor(self._hass_instance,self._hass_instance.states[state]))


    def _initialize_devices(self):
        """
        | Initializes the devices and links the sensors and actuators to them
        """
        for device in self._hass_instance.device_registry:
            self._devices[device] = Device(self._hass_instance.device_registry[device])

    async def connect(self):
        """
        | Establish connection to the homeassistant server
        """
        await self._hass_instance.connect()
        self._initialize_devices()

        self._initialize_sensors()
        self._initialize_binary_sensors()
        self._initialize_switches()
        self._initialize_lights()
        self._initialize_image_processors()
        self._clean_empty_devices()
        print('Connection established')

    async def disconnect(self):
        """
        | Disconnects from the homeassistant server
        """
        await self._hass_instance.disconnect()

    def _clean_empty_devices(self):
        keys_to_remove = []
        for key in self._devices:
            if self._devices[key].is_empty():
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self._devices[key]

    def get_sensors(self, sensor_class: SensorClass) -> [StandardSensor]:
        """
        | Gets the list of sensors present in homeassistant by Sensor class

        :param sensor_class: The Sensor Class to look for

        :type sensor_class: SensorClass
        :return: List of sensors of the specified class
        :rtype: [StandardSensor]
        """
        return self._sensors[sensor_class]

    def get_binary_sensors(self, binary_sensor_class: BinarySensorClass) -> [BinarySensor]:
        """
        | Gets the list of binary sensors present in homeassistant by Sensor class

        :param binary_sensor_class: The Sensor Class to look for
        :type binary_sensor_class: BinarySensorClass

        :return: List of sensors of the specified class
        :rtype: [BinarySensor]
        """
        return self._binary_sensors[binary_sensor_class]

    def get_lights(self) -> [Light]:
        """
        | Gets the list of lights present in homeassistant

        :return: List of lights
        :rtype: [Light]
        """
        return self._lights

    def get_switches(self) -> [Switch]:

        """
        | Gets the list of switches present in homeassistant

        :return: List of switches of the specified class
        :rtype: [Switch]
        """
        return self._switches

    def get_sensor_by_entity_id(self, entity_id: str) -> StandardSensor:
        for sensor_cat in self._sensors:
            for sensor in self._sensors[sensor_cat]:
                if sensor.get_entity_id() == entity_id:
                    return sensor
        raise NameError

    def get_binary_sensor_by_entity_id(self, entity_id: str) -> BinarySensor:
        for sensor_cat in self._binary_sensors:
            for sensor in self._binary_sensors[sensor_cat]:
                if sensor.get_entity_id() == entity_id:
                    return sensor
        raise NameError

    def get_light_by_entity_id(self, entity_id: str) -> Light:
        for light in self._lights:
            if light.get_entity_id() == entity_id:
                return light
        raise NameError

    def get_switch_by_entity_id(self, entity_id: str) -> Switch:
        for switch in self._switches:
            if switch.get_entity_id() == entity_id:
                return switch
        raise NameError

    def print_devices_info(self) -> None:
        for device in self._devices:
            dev: Device = self._devices[device]
            print("DEVICE: " + dev.name)

            for sensor in dev.get_standard_sensors():
                print("   " + sensor.sensor_class.value[0] + " sensor -> " + sensor.get_entity_id())
            for binary_sensor in dev.get_binary_sensors():
                print("   " + binary_sensor.sensor_class.value[0] + " binary sensor -> " + binary_sensor.get_entity_id())
            for light in dev.get_lights():
                print("   " + "Light -> " + light.get_entity_id())
            for switch in dev.get_switches():
                print("   " + "Switch -> " + switch.get_entity_id())

    async def set_text_title(self, text: str) -> None:
        """
        | Sets the text card title
        | Must be awaited
        :param text: Title text
        :type sensor: str

        """
        await self._hass_instance.call_service("input_text", 'set_value',
                                               {'entity_id': 'input_text.title', 'value': text})

    async def set_text_content(self, text: str) -> None:
        """
        | Sets the text card content
        | Must be awaited
        :param text: Content text
        :type sensor: str

        """
        await self._hass_instance.call_service("input_text", 'set_value',
                                               {'entity_id': 'input_text.content', 'value': text})

    async def sleep(self, seconds: float):

        """
        | Stops the program fot the defined time
        | Must be awaited

        :param seconds: Time to sleep
        :type seconds: float
        """
        await asyncio.sleep(seconds)

    async def say(self, message: str, language: str = 'en', media_player_entity: str = 'media_player.mpd') -> None:
        """
        | Play text to speech through a media server
        | Must be awaited

        :param message: Text to say
        :type message: str

        :param language: Language identifier
        :type language: str

        :param media_player_entity: Media player id
        :type media_player_entity: str
        """
        try:
            await self._hass_instance.call_service("tts", 'google_say',
                                                   {'entity_id': media_player_entity,
                                                    'language': language,
                                                    'message': message
                                                    })
        except:
            print("Already playing text to speech")

    def _manage_hass_event(self, event, event_details):
        # LOGGER.info("received event %s --> %s\n", event, event_details)
        pass

    def _create_sensor(self, sensor: dict):
        """
        | Creates a StandardSensor instance using the dictionary from homeassistant

        :param sensor: Dictionary with the sensor information
        :type sensor: Dict

        :return: StandardSensor instance
        :rtype: StandardSensor
        """
        if sensor['attributes']['device_class'] == SensorClass.BATTERY.value[0]:
            return BatterySensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == SensorClass.HUMIDITY.value[0]:
            return HumiditySensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == SensorClass.ILLUMINANCE.value[0]:
            return IlluminanceSensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == SensorClass.TEMPERATURE.value[0]:
            return TemperatureSensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == SensorClass.SIGNAL_STRENGTH.value[0]:
            return SignalStrengthSensor(self._hass_instance, sensor)

        elif sensor['attributes']['device_class'] == SensorClass.CARBON_DIOXIDE.value[0]:
            return CO2Sensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == SensorClass.PRESSURE.value[0]:
            return PressureSensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == SensorClass.CURRENT.value[0]:
            return CurrentSensor(self._hass_instance, sensor)

        # elif sensor['attributes']['device_class'] == SensorClass.:
        #            pass
        # elif sensor['attributes']['device_class'] == SensorClass.:
        #            pass
        else:
            pass

    def _create_binary_sensor(self, sensor: dict):
        """
        | Creates a BinarySensor instance using the dictionary from homeassistant

        :param sensor: Dictionary with the sensor information
        :type sensor: Dict

        :return: BinarySensor instance
        :rtype: BinarySensor
        """
        if sensor['attributes']['device_class'] == BinarySensorClass.MOTION.value[0]:
            return MotionSensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == BinarySensorClass.OCCUPANCY.value[0]:
            return OccupancySensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == BinarySensorClass.PROBLEM.value[0]:
            return ProblemSensor(self._hass_instance, sensor)

        elif sensor['attributes']['device_class'] == BinarySensorClass.OPENING.value[0]:
            return OpeningSensor(self._hass_instance, sensor)

        elif sensor['attributes']['device_class'] == BinarySensorClass.HEAT.value[0]:
            return HeatSensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == BinarySensorClass.IAS_ZONE.value[0]:
            return IasZoneSensor(self._hass_instance, sensor)
        elif sensor['attributes']['device_class'] == BinarySensorClass.SOUND.value[0]:
            return SoundSensor(self._hass_instance, sensor)

        # elif sensor['attributes']['device_class'] == SensorClass.:
        #            pass
        # elif sensor['attributes']['device_class'] == SensorClass.:
        #            pass
        # elif sensor['attributes']['device_class'] == SensorClass.:
        #            pass
        # elif sensor['attributes']['device_class'] == SensorClass.:
        #            pass
        else:
            pass
