import logging
from enum import Enum
from datetime import datetime

def log_function_call(func):
    """
    Function decorator to apply consistent logging
    
    """
    def wrapper(*args, **kwargs):
        logging.info(f"Function '{func.__name__}' called with arguments: {args} and keyword arguments: {kwargs}")
        return func(*args, **kwargs)
    return wrapper


def format_date(date: datetime) -> str:
    """
    Formats a datetime object into a consistent string format: 'YYYY-MM-DD HH:MM:SS'.

    Args:
        date (datetime): The datetime object to be formatted.

    Returns:
        str: The formatted datetime string.

    Raises:
        TypeError: If the input is not a datetime object.
    """
    if not isinstance(date, datetime):
        raise TypeError("Input must be a datetime object.")
    
    return date.strftime("%Y-%m-%d %H:%M:%S")

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

