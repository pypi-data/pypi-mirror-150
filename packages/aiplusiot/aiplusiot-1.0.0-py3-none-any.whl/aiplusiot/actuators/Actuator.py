from hass_client import HomeAssistantClient


class Actuator:
    def __init__(self, hass_instance: HomeAssistantClient, entity_id: str) -> None:

        """
        | Create an Actuator instance from homeassistant data

        :param hass_instance: Instance of homeassistant client library
        :type hass_instance: HomeAssistantClient

        :param entity_id: Id of the actuator entity
        :type entity_id: str
        """
        self._hass_instance = hass_instance
        self.entity_id = entity_id
        self.entity_data = hass_instance.entity_registry[entity_id]



