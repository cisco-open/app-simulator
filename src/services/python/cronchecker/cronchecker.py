from datetime import datetime

## This checker only supports classical cron notation with 5 field
##
## * * * * * 
## | | | | |  
## | | | | | 
## | | | | +---- Day of the Week   (range: 1-7, 1 standing for Monday)
## | | | +------ Month of the Year (range: 1-12)
## | | +-------- Day of the Month  (range: 1-31)
## | +---------- Hour              (range: 0-23)
## +------------ Minute            (range: 0-59)
##

def match_cron_field(cron_field, value):
    """Check if the specific field in the cron pattern matches the current time value."""
    # Split on commas first to handle multiple conditions
    for part in cron_field.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            if start <= value <= end:
                return True
        elif '/' in part:
            base, step = part.split('/')
            if base == '*':
                if value % int(step) == 0:
                    return True
            else:
                base = int(base)
                if value == base or (value - base) % int(step) == 0:
                    return True
        elif part == '*':
            return True
        elif value == int(part):
            return True
    return False

def is_time_matching_cron(cron_string, current_time=None):
    """
    Check if the current time matches the cron schedule.

    :param cron_string: A string representing the cron schedule (e.g., "*/5 * * * *").
    :param current_time: A datetime object representing the current time. If None, use the current system time.
    :return: True if the current time matches the cron schedule, False otherwise.
    """
    if current_time is None:
        current_time = datetime.now()

    cron_parts = cron_string.split()
    if len(cron_parts) != 5:
        raise ValueError("Cron string must have exactly 5 fields.")

    minute, hour, day_of_month, month, day_of_week = cron_parts

    return (match_cron_field(minute, current_time.minute) and
            match_cron_field(hour, current_time.hour) and
            match_cron_field(day_of_month, current_time.day) and
            match_cron_field(month, current_time.month) and
            match_cron_field(day_of_week, current_time.weekday()+1)) ## weekday in python starts with 0 where as in cron its 1 

