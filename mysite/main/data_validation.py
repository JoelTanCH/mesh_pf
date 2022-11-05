def validate_data(data, data_type, data_optional=False, valid_range=None, min_value=None, max_value=None):
    # Check for missing data
    missing = validate_missing_data(data)
    if missing:
        if data_optional:
            return ("")
        return ("Data missing")
    # Check for data type
    valid_type = validate_data_type(data, data_type)
    if not valid_type:
        return ("Invalid data type")
    # Check for valid acceptable data value, either min max range or list of values
    if valid_range is not None and min_value is not None and max_value is not None:
        data_value = validate_data_value(data, valid_range, min_value, max_value)
    
    else:
        return ("")
   
    if data_value is None:
        return ("Invalid data range provided")
    if data_value is False:
        return ("Data is not within acceptable range of values")

    return ("")


def validate_data_value(data, valid_range=None, min_value=None, max_value=None):
    if valid_range is None and min_value is None and max_value is None:
        return None
    elif valid_range is not None:
        if valid_range == []:
            return None
        return validate_data_valid_range(data, valid_range)
    else:
        if min_value is None and max_value is None:
            return None
        return validate_data_value_range(data, min_value, max_value)


def validate_data_value_range(data, min_value, max_value):
    if not (isinstance(data, int) or isinstance(data, float)):
        return None
    above_min = True
    below_max = True
    if min_value is not None:
        above_min = True if data >= min_value else False
    if max_value is not None:
        below_max = True if data <= max_value else False
    return (above_min and below_max)


def validate_data_valid_range(data, valid_range):
    if not isinstance(valid_range, list):
        return None
    if data in valid_range:
        return True
    else:
        if isinstance(data, str):
            if any([isinstance(x, str) for x in valid_range]):
                lower_valid_range = [x.lower() 
                    if isinstance(x, str)
                    else x
                    for x in valid_range]
                if data.lower() in lower_valid_range:
                    return True
    return False


# should only have float and string tyoes
def validate_data_type(data, data_type):
    if data_type == "str":
        return isinstance(data, str)
    elif data_type == "float":
        return isinstance(data, float)
    return False
    # if isinstance(data, data_type):
    #     return True
    # return False


def validate_missing_data(data):
    if data is None:
        return True
    if data == "":
        return True
    return False



