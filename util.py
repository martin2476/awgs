from enum import Enum

class FlightStatus(Enum):
    SCHEDULED = 1
    DELAYED = 2
    CANCELLED = 3
    BOARDING = 4
    DEPARTED = 5
    LANDED = 6
