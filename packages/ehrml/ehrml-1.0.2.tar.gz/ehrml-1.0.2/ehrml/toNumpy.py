# condert data into the expected numpy format
import numpy

def _locf_impute(data):
    """Impute data using the last observation carried forward method.
       If the first value is None, it will be set to zero first.

    Args:
        data:
            list of data in chronological order, where `None` represents missing
            data.

    Returns:
        Data in the same format as the input, with `None` replaced.

    """
    if data[0] is None:
        data[0] = 0
    for i in range(len(data)):
        if data[i] is None:
            data[i] = data[i-1]
    return data


def _none_impute(data):
    """Do not impute data. Placeholder.

    Args:
        data:
            list of data in chronological order, where `None` represents missing
            data.

    Returns:
        The exact data from the input with no change.

    """
    return data

_imputation_options = {'none':_none_impute, 'locf': _locf_impute}

def toNumpyRecord(config, data, shape, impute="locf"):
    """Convert binned data into a numpy format, optionally imputing.

    Args:
        config:
            list of dicts, each containing configuration for a field of interest.
        data:
            A list of dicts representing bins, each with values associated with
            the time range that bin represents.
        shape:
            The desired shape of the numpy output, tuple (observations, indices)
        impute:
            A string representing which imputation method to use.
            See `_imputation_options`.

    Returns:
        A numpy array where each column represents a variable index, and each
        row represents an observation.

    """
    res = numpy.zeros(shape)
    for c in config:
        d = [x.get(c.get('rwb_src'), None) for x in data]
        # expand one hots
        if type(d[0]) is list:
            for i in range(len(d)):
                if d[i]:
                    for j in range(len(d[i])):
                        res[i, int(c.get('index')) + j] = d[i][j]
        else:
            # set missing flags
            if c.get('missing_flag_index'):
                res[:, int(c.get('missing_flag_index'))] = [1 if x is None else 0 for x in d]
            # impute
            d = _imputation_options[impute](d)
            # set results in res
            res[:, int(c.get('index'))] = d
    return res

def numpyRecordCollector(records):
    """Collect multiple numpy arrays together.

    Args:
        records:
            list of numpy arrays of the same shape, each representing a patient
            or other entity of interest.
    Returns:
        A numpy 3d array, with the first dimension representing each record of
        the input, the second dimension representing observations, and the third
        dimension representing variable indices.

    """
    x, y = records[0].shape
    res = numpy.zeros((len(records), x, y))
    for i in range(len(records)):
        res[i, :, :] = records[i]
    return res
