


'''
Various utilities for normalizing types
'''



def to_str_or_none(value: str | float | int | None) -> str | None:
    '''
    Attempts to convert value to a string \n
    Returns None if value is already None or there is an error \n
    Raises AttributeError if value is not a float, int or already a string

    Args:
        value (str | float | int | None): The value

    Returns:
        str | None: Value as string, None
    
    Raises:
        AttributeError: If value is not (str | float | int | None)
    '''
    # Return None if the value is already None
    if value is None:
        return None
    
    # Raise error if the value is not a convertible type
    if not isinstance(value, (str, float, int)):
        raise AttributeError(f"Cannot convert value of type {type(value)} to string")

    # Propagate the exception if there is a different error
    return str(value)



def to_float_or_none(value: str | float | int | None) -> float | None:
    '''
    Attempts to convert value to a float \n
    Returns None if value is already None or there is an error \n
    Raises AttributeError if value is not a string, int or already a float

    Args:
        value (str | float | int | None): The value

    Returns:
        float | None: Value as float or None
    
    Raises:
        AttributeError: If value is not (str | float | int | None)
    '''
    # Return None if the value is already None
    if value is None:
        return None
    
    # Raise error if the value is not a convertible type
    if not isinstance(value, (str, float, int)):
        raise AttributeError(f"Cannot convert value of type {type(value)} to float")
    
    # Propagate the exception if there is a different error
    return float(value)


def to_int_or_none(value: str | float | int | None) -> int | None:
    '''
    Attempts to convert value to a int \n
    Returns None if value is already None or there is an error \n
    Raises AttributeError if value is not a string, float or already a int

    Args:
        value (str | float | int | None): The value

    Returns:
        int | None: Value as int or None
    
    Raises:
        AttributeError: If value is not (str | float | int | None)
    '''
    # Return None if the value is already None
    if value is None:
        return None
    
    # Raise error if the value is not a convertible type
    if not isinstance(value, (str, float, int)):
        raise AttributeError(f"Cannot convert value of type {type(value)} to float")
    
    # Propagate the exception if there is a different error
    return int(value)


def to_bool_or_none(value: str | None) -> bool | None:
    '''
    Attempts to convert value to a bool \n
    Returns None if value is already None or there is an error \n
    Raises AttributeError if value is not a string or already a bool

    Args:
        value (str | None): The value

    Returns:
        bool | None: Value as bool or None
    
    Raises:
        AttributeError: If value is not (str | None)
    '''
    # Return None if the value is already None
    if value is None:
        return None
    
    # Raise error if the value is not a convertible type
    if not isinstance(value, (str, bool)):
        raise AttributeError(f"Cannot convert value of type {type(value)} to bool")
    
    # Propogate the exception if there is a different error
    return bool(value)


def to_list_of_str(values: list | None) -> list[str] | list:
    '''
    Attempts to convert value to a list of strings \n
    Returns an empty list if value is None \n
    Raises AttributeError if value is not a list

    Args:
        value (list | None): The list of values

    Returns:
        list[str] | list: Values as list of string or empty list
    
    Raises:
        AttributeError: If value is not a list
    '''
    if values is None:
        return []
    if isinstance(values, list):
        if len(values) > 0:
            return [str(value) for value in values]
        else:
            return []
    else:
        raise AttributeError("Provide values is not a list")


def to_list_of_float(values: list | None) -> list[float] | list:
    '''
    Attempts to convert value to a list of floats \n
    Returns an empty list if value is None \n
    Raises AttributeError if value is not a list

    Args:
        value (list | None): The list of values

    Returns:
        list[float] | list: Values as list of floats or empty list
    
    Raises:
        AttributeError: If value is not a list
    '''
    if values is None:
        return []
    if isinstance(values, list):
        if len(values) > 0:
            return [float(value) for value in values]
        else:
            return []
    else:
        raise AttributeError("Provided value is not a list")