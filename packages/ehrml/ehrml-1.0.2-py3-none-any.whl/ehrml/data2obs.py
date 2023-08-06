#functions which transform data to observations
import datetime
import math
from .utils import readTime

def fromLayered(config, data):
    """Use configuration to extract data from a layered format into a list of observations.

    Args:
        config:
            list of dicts, each containing configuration for a field of interest.
        data:
            the layered data structure, a dict with keys matching config's
            "api_parent" with values in a list. Values should be either directly
            accessable from config's "api_src", with associated time in config's
            "api_time_src", or alternatively by config's "api_from" where
            the value associated with config's "api_by" matches config's
            "api_src"

    Returns:
        A list of dicts representing observations, each with its value, field,
            and time.

    """
    res = []
    for conf in config:
        all_relevant = []
        if conf.get('api_by') and conf.get('api_from'):
            # handle as a list-type item
            all_relevant = [
                    {'value': x.get(conf.get('api_from'), conf.get('api_src')),
                     'field': conf.get('rwb_src'),
                     'time': readTime(x.get(conf.get('api_time_src')))}
                    for x in data.get(conf.get('api_parent'), [])
                    if x.get(conf.get('api_by')) and x.get(conf.get('api_by')) == conf.get('api_src') and x.get(conf.get('api_from'))
                ]
        else:
            # handle as a direct-fetch item
            all_relevant = [
                    {'value': x.get(conf.get('api_src'), conf.get('api_src')),
                     'field': conf.get('rwb_src'),
                     'time': readTime(x.get(conf.get('api_time_src')))}
                    for x in data.get(conf.get('api_parent'), [])
                    if x.get(conf.get('api_src'))
                ]
        res.extend(all_relevant)
    return res

def fromFlat(config, data, time_limit=None):
    """Use configuration to extract data from a flat list of dicts, possibly
       containing time related fields.

    Args:
        config:
            list of dicts, each containing configuration for a field of interest.
        data:
            the flat data structure, a list of dicts matching either config's
            "rwb_src" or the same with a time range asscoiated. (e.g.
            Calcium_08_16 would mean calcium somwewhere between 08:00 and 16:00)
        time_limit (optional):
            An override to which time range in the day to read up to. This is a
            testing override.

    Returns:
        A list of dicts representing observations, each with its value, field,
            and time.

    """
    time_delimter = "_"
    time_ranges = ["00_08", "08_16", "16_MN"] # MUST be in order and equally spaced, occuping an entire day.
    hour_per_range = 24./len(time_ranges)
    # time override option to allow an override for time for testing purposes
    time_limit = time_limit or math.floor(datetime.datetime.now().hour / hour_per_range)
    res = []
    for i in range(time_limit):
        # the range to read and time to "write" for this range
        current_range = time_ranges[i]
        write_time = datetime.datetime.now().replace(hour=int((i+1)*hour_per_range)-1, minute=59, second=59, microsecond=0)
        for conf in config:
            # add the field to this range if it is timeless
            if conf.get('rwb_src') in data:
                res.append({'value': data[conf.get('rwb_src')],
                 'field': conf.get('rwb_src'),
                 'time': write_time})
            # add the field to this range if it matches the current range
            if conf.get('rwb_src') + time_delimter + current_range in data:
                res.append({'value': data[conf.get('rwb_src') + time_delimter + current_range],
                 'field': conf.get('rwb_src'),
                 'time': write_time})
    return res
