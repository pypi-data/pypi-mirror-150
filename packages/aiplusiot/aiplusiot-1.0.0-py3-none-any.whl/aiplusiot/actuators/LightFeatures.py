from enum import Enum


class LightFeatures(Enum):
    # Bitfield of features supported by the light entity
    SUPPORT_BRIGHTNESS = 1,
    SUPPORT_COLOR_TEMP = 2,
    SUPPORT_EFFECT = 4,
    SUPPORT_FLASH = 8,
    SUPPORT_COLOR = 16,
    SUPPORT_TRANSITION = 32,
    SUPPORT_WHITE_VALUE = 128,
