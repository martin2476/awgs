import logging
from enum import Enum

# Function decorator to apply consistent logging
def log_function_call(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Function '{func.__name__}' called with arguments: {args} and keyword arguments: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

class FlightStatus(Enum):
    SCHEDULED = 1
    DELAYED = 2
    CANCELLED = 3
    BOARDING = 4
    DEPARTED = 5
    LANDED = 6



class ActiveStatus(Enum):
    INACTIVE = 0
    ACTIVE = 1


def get_active_flight_statuses():
    """
    Returns an array containing a list of Status which an Active flight could have
    
    return (Scheduled,Departed,Boarding,Delayed,Landed)
    """    
    active_statuses = [
        FlightStatus.SCHEDULED.value, 
        FlightStatus.DEPARTED.value, 
        FlightStatus.BOARDING.value, 
        FlightStatus.DELAYED.value, 
        FlightStatus.LANDED.value
    ]
    return f"({','.join(map(str, active_statuses))})"

