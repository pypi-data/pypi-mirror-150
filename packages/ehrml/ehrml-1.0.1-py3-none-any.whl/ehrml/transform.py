import math
import json

from .utils import truthy_values

# binary transformations
def _binary(value, one_hot_vals):
    return 1.0 if value in truthy_values else 0.0

def _cutoffs(value, one_hot_vals):
    cutoffs = json.loads(one_hot_vals)
    if value is None:
        value = [0] * len(cutoffs)
    else:
        ov = value
        new_value = [0] * len(cutoffs)
        for c in cutoffs:
            if value > c:
                new_value = [0] * len(cutoffs)
                new_value[cutoffs.index(c)] = 1
        value = new_value
    return value

def _categorical(value, one_hot_vals):
    categories = json.loads(one_hot_vals)
    if value is None:
        value = [0] * len(categories)
    else:
        new_value = [1 if value in x else 0 for x in categories]
        value = new_value
    return value

# numeric transformations
def _zScore(value, mean, std, max, min):
    print(value, mean, std, max, min, (value - mean) / std)
    return (value - mean) / std

def _high(value, mean, std, max, min):
    return ((max - value + 1)- mean) / std

def _low(value, mean, std, max, min):
    return ((value - min + 1)- mean) / std

def _sqrtHigh(value, mean, std, max, min):
    return (math.sqrt(max - value + 1) - mean) / std

def _sqrtLow(value, mean, std, max, min):
    return (math.sqrt(value - min + 1) - mean) / std

def _logLow(value, mean, std, max, min):
    return (math.log(value - min + 1) - mean) / std

def _logHigh(value, mean, std, max, min):
    return (math.log(max - value + 1) - mean) / std

_bin_tx = {'binary': _binary, 'cutoffs': _cutoffs, 'categorical': _categorical}
_num_tx = {'z': _zScore, 'low': _low, 'high': _high, 'sqrt low': _sqrtLow, 'sqrt high': _sqrtHigh, 'log low': _logLow, 'log high': _logHigh}

def transform(config, binnedData):
    """Perform numerical transformations and one hot encoding on binned data.
       Some specific transformations are supported, see the source and `_num_tx`
       for a list of supported transformations and their config names.
       Similarly, some specific one hot encoding methods are supported, see the
       source and `_bin_tx` for a list of supported encodigs and their config
       names. NOTE that numerical errors in a transformation return a 0 for that
       particular transformation instance.

    Args:
        config:
            list of dicts, each containing configuration for a field of interest.
        binnedData:
            A list of dicts representing bins, each with values associated with
            the time range that bin represents.

    Returns:
        A list of dicts representing bins, each with values associated with
        the time range that bin represents, with values transformed or encoded
        per config.

    """
    res = []
    keyedConf = {x.get('rwb_src'): x for x in config}
    for b in binnedData:
        bRes = {}
        for k, c in keyedConf.items():
            try:
                if c.get('transformation', 'none') in _bin_tx:
                    bRes[k] = _bin_tx[c.get('transformation')](b[k], c.get('one_hot_vals'))
                elif c.get('transformation', 'none') in _num_tx:
                    if b[k]:
                        pre_tx = float(b[k])
                        if c.get('min') and c.get('max'):
                            # set within [min,max]
                            pre_tx = max(min(float(c.get('max')), pre_tx), float(c.get('min')))
                        bRes[k] = _num_tx[c.get('transformation')](pre_tx, float(c.get('mean')), float(c.get('std')), float(c.get('max')), float(c.get('min')))
                    else:
                        bRes[k] = b[k]
            except ValueError as e:
                print(e)
                # numerical error, manual 0
                bRes[k] = 0
        res.append(bRes)
    return res
