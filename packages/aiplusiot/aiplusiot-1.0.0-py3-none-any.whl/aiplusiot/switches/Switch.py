from hass_client import HomeAssistantClient


class Switch():
    def __init__(self, hass_instance: HomeAssistantClient, switch_info):
        """
        | Initializes a Switch using a switch data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param switch_info: Sensor data dictionary
        :type switch_info: dict
        """

        self._hass_instance = hass_instance
        self._raw_switch_info = switch_info
        self._entity_id = switch_info['entity_id']
        self._friendly_name = switch_info['attributes']['friendly_name']
        self._string_state = switch_info['state']
        if self._string_state == 'on':
            self.bool_state = True
        else:
            self.bool_state = False
        self._hass_instance.register_event_callback(self._process_hass_event)

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
        return self._friendly_name

    def get_state(self):
        return self.bool_state



    async def turn_on(self):
        await self._hass_instance.call_service("switch", 'turn_on',
                                               {'entity_id': self._entity_id})

    async def turn_off(self):
        await self._hass_instance.call_service("switch", 'turn_off',
                                               {'entity_id': self._entity_id})

    async def toggle(self):
        await self._hass_instance.call_service("switch", 'toggle',
                                               {'entity_id': self._entity_id})

    async def _process_hass_event(self, event, event_details):

        """
        | Process events from homeassistant and filter them

        :param event: Type of event
        :type event: str

        :param event_details: Event data dictionary
        :type event_details: dict
        """
        if event == 'state_changed':
            if event_details['entity_id'] == self._entity_id:
                print('Event! ' + str(event_details))
                self.state = event_details['new_state']['state']
                if self._string_state == 'on':
                    self.bool_state = True
                else:
                    self.bool_state = False
