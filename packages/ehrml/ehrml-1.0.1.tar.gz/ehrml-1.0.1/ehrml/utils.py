# utilities which are not exposed to the user
import datetime

def readTime(s):
    """Read the time from a string in a particular format.

    Args:
        s: The representing datetime.

    Returns:
        A datetime object.
    """
    if s:
        fs = "%Y-%m-%dT%H:%M:%S"
        return datetime.datetime.strptime(s, fs)
    else:
        return s

truthy_values =  ['y', 'Y', 'true', 'YES', 'Yes', 'yes', 1, '1', '1.0', True, 1.0]
