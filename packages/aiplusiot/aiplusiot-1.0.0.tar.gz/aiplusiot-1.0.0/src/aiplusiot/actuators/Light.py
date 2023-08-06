import colorsys

from hass_client import HomeAssistantClient

from aiplusiot.actuators.Actuator import Actuator
from aiplusiot.actuators.LightFeatures import LightFeatures


class Light(Actuator):
    def __init__(self, hass_instance: HomeAssistantClient, light_info: dict) -> None:
        """
        | Initializes a Light using a light data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param light_info: Light data dictionary
        :type light_info: dict
        """
        self.raw_light_info = light_info
        self._state = light_info['state']
        self._supported_color_modes = light_info['attributes']['supported_color_modes']
        self._color_mode = ''
        self._entity_id = light_info['entity_id']

        if self._state == 'on':
            self.brightness = light_info['attributes']['brightness']
            self.color_rgb = light_info['attributes']['rgb_color']
        self._friendly_name = light_info['attributes']['friendly_name']
        self._supported_features = light_info['attributes']['supported_features']
        super().__init__(hass_instance, light_info['entity_id'])
        self._hass_instance.register_event_callback(self._process_hass_event)

    def get_entity_id(self) -> str:
        """
        | Gets the entity id of the sensor


        :return: Entity id
        :rtype: str
        """
        return self._entity_id

    def is_on(self):
        return self._state == 'on'

    def get_name(self) -> str:
        """
        | Gets the entity id of the sensor


        :return: Entity id
        :rtype: str
        """
        return self._friendly_name

    async def turn_on(self) -> None:
        """
        | Turn on the light
        """
        await self._hass_instance.call_service("light", 'turn_on', {'entity_id': self.entity_id})

    async def turn_off(self) -> None:

        """
        | Turn off the light
        """
        await self._hass_instance.call_service("light", 'turn_off', {'entity_id': self.entity_id})

    async def set_color(self, rgb_color: list, brightness: int = None) -> None:

        """
        | Sets the light color

        :param rgb_color: Color in [r, g, b] format
        :type rgb_color: list

        :param brightness: Brightness in percentage
        :type brightness: int
        """
        if 'rgb' in self._supported_color_modes:
            if brightness is None:
                await self._hass_instance.call_service("light", 'turn_on',
                                                       {'entity_id': self.entity_id, 'rgb_color': rgb_color})
            else:
                await self._hass_instance.call_service("light", 'turn_on',
                                                       {'entity_id': self.entity_id, 'rgb_color': rgb_color,
                                                        'brightness_pct': brightness})
        elif 'hs' in self._supported_color_modes:
            hs = convert_rgb_to_hs(rgb_color)
            await self.set_color_hs(hs)
        else:
            print("Color not supported in this light")

    async def set_color_hs(self, hs_color: list, brightness: int = None) -> None:

        """
        | Sets the light color

        :param rgb_color: Color in [r, g, b] format
        :type rgb_color: list

        :param brightness: Brightness in percentage
        :type brightness: int
        """
        if 'hs' in self._supported_color_modes:
            if brightness is None:
                await self._hass_instance.call_service("light", 'turn_on',
                                                       {'entity_id': self.entity_id, 'hs_color': hs_color})
            else:
                await self._hass_instance.call_service("light", 'turn_on',
                                                       {'entity_id': self.entity_id, 'hs_color': hs_color,
                                                        'brightness_pct': brightness})
        else:
            print("Color hs not supported in this light")

    async def set_temperature(self, kelvin: int, brightness: int = None) -> None:

        """
        | Sets the light temperature

        :param rgb_color: Temperature in kelvin
        :type rgb_color: int

        :param brightness: Brightness in percentage
        :type brightness: int
        """
        if 'color_temp' in self._supported_color_modes:
            if brightness is None:
                await self._hass_instance.call_service("light", 'turn_on',
                                                       {'entity_id': self.entity_id, 'kelvin': kelvin})
            else:
                await self._hass_instance.call_service("light", 'turn_on',
                                                       {'entity_id': self.entity_id, 'kelvin': kelvin,
                                                        'brightness_pct': brightness})
        else:
            print("Color temperature not supported in this light")

    async def set_brightness(self, brightness: int) -> None:
        """
        | Sets the light brightness

        :param brightness: Brightness in percentage
        :type brightness: int
        """
        # if LightFeatures.SUPPORT_BRIGHTNESS in self.supported_color_modes:
        await self._hass_instance.call_service("light", 'turn_on',
                                               {'entity_id': self.entity_id,
                                                'brightness_pct': brightness})
        # else:
        #    print("Brightness not supported in this light")

    async def _process_hass_event(self, event: str, event_details: dict) -> None:
        """
        | Process events from homeassistant and filter them

        :param event: Type of event
        :type event: str

        :param event_details: Event data dictionary
        :type event_details: dict
        """

        if event == 'state_changed':
            if event_details['entity_id'] == self.entity_id:
                self._state = event_details['new_state']['state']
                if self._state == 'on':
                    self.brightness = event_details['new_state']['attributes']['brightness']
                    self.color_rgb = event_details['new_state']['attributes']['rgb_color']


def convert_rgb_to_hs(rgb_color):
    # rgb normal: range (0-255, 0-255, 0.255)
    red = rgb_color[0]
    green = rgb_color[1]
    blue = rgb_color[2]

    # get rgb percentage: range (0-1, 0-1, 0-1 )
    red_percentage = red / float(255)
    green_percentage = green / float(255)
    blue_percentage = blue / float(255)

    # get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage = colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage)
    print('color_hsv_percentage: ', color_hsv_percentage)

    # get normal hsv: range (0-360, 0-255, 0-255)
    color_h = round(360 * color_hsv_percentage[0])
    color_s = round(100 * color_hsv_percentage[1])
    color_v = round(255 * color_hsv_percentage[2])
    color_hs = [color_h, color_s]
    return color_hs
