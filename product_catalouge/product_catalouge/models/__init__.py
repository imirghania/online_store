from enum import Enum


class AttributeType(Enum):
    SELECT = 'select'
    NUMBER = 'number'
    STRING = 'string'


class MeasurmentType(Enum):
    DISTANCE = 'distance'
    WEIGHT = 'weight'
    VOLUME = 'volume'