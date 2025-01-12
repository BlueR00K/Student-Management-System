from typing import Any, Hashable, Iterable


def search(data_list: Iterable[dict], key: Hashable, value: Any) -> dict[str, Any]:
    """
    Searches for dictionaries in a list that contain a specific key-value pair.
    Args:
        data_list (Iterable[dict]): A list of dictionaries to search through.
        key (Hashable): The key to look for in each dictionary.
        value (Any): The value associated with the key to match.
    Returns:
        dict[str, Any]: A dictionary containing:
            - 'SUCCESS' (bool): True if at least one match is found, False otherwise.
            - 'ERR_MSG' (dict): Contains an error message if no match is found.
            - 'SUC_MSG' (dict): Currently unused, reserved for success messages.
            - 'RETURN' (list): A list of dictionaries that match the key-value pair.
    """
    
    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': []
    }

    for data in data_list:
        if data[key] == value:
            function_result['RETURN'].append(data)

    if not function_result['RETURN']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['KEY'] = f'{value} doesn\'t exist in database' 

    return function_result
