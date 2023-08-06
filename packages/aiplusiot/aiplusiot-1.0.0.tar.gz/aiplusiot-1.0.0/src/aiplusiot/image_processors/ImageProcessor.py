from hass_client import HomeAssistantClient


class ImageProcessor:
    def __init__(self, hass_instance: HomeAssistantClient, imgproc_info: dict) -> None:
        """
        | Initializes a sensor using a sensor data dict

        :param hass_instance: Instance of the HomeAssistant Client
        :type hass_instance: HomeAssistantClient

        :param sensor_info: Sensor data dictionary
        :type sensor_info: dict
        """

        self._raw_imgproc_info = imgproc_info
        self._entity_id = imgproc_info['entity_id']
        self.state = imgproc_info['state']
        self.detections_summary = imgproc_info['attributes']['summary']

        self._hass_instance = hass_instance


    def get_entity_id(self) -> str:
        """
        | Gets the entity id of the sensor


        :return: Entity id
        :rtype: str
        """
        return self._entity_id

    def get_state(self) -> str:
        """
        | Gets the entity id of the sensor


        :return: Entity id
        :rtype: str
        """
        return self.state
    def get_detections_summary(self) -> str:
        """
        | Gets detection summary of the sensor


        :return: Entity id
        :rtype: str
        """
        return self.state
    async def _update_fields(self, event_details: dict) -> None:
        """
        | Updates the sensor data

        :param event_details: Event that triggered the update
        :type event_details: dict
        """
        self.state = self._hass_instance.states[self._entity_id]['state']
        self.detections_summary = self._hass_instance.states[self._entity_id]['summary']
