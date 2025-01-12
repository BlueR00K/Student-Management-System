from typing import Literal
from os.path import isfile

# student = {
#     'name': None,
#     'family': None,
#     'birth': None,
#     'gender': None,
#     'ncode': None,
#     'stdcode': None
# }

__all__ = ['write_line', 'write_list', 'read_all']

# region write line


def write_line(path: str, data: dict, mode: Literal['a', 'w'] = 'a'):
    """
    Writes a line of data to a file.
    Args:
        path (str): The file path where the data should be written.
        data (dict): The data to be written to the file.
        mode (Literal['a', 'w'], optional): The mode in which to open the file. 
            'a' for append and 'w' for write. Defaults to 'a'.
    Returns:
        dict: A dictionary containing the result of the operation with the following keys:
            - 'SUCCESS' (bool): Indicates if the operation was successful.
            - 'ERROR_MSG' (dict): Contains error messages if any occurred.
            - 'SUCCESS_MSG' (dict): Contains success messages if any.
            - 'RETURN' (Any): The return value, typically the error if one occurred.
    """


    function_result = {
        'SUCCESS': True,
        'ERROR_MSG': {},
        'SUCCESS_MSG': {},
        'RETURN': None
    }

    file_object = None

    try:
        file_object = open(file=path, mode=mode)
        file_object.write(data)
    except BaseException as error:
        function_result['SUCCESS'] = False
        function_result['ERROR_MSG']['file_error'] = f'{error}'
        function_result['RETURN'] = error
        return function_result
    else:
        return function_result
    finally:
        if file_object and not file_object.closed:
            file_object.close()

# endregion

# region wite list


def write_list(path: str, data: dict, mode: Literal['a', 'w'] = 'a'):
    """
    Writes a dictionary to a file.
    Args:
        path (str): The path to the file where the data should be written.
        data (dict): The dictionary data to be written to the file.
        mode (Literal['a', 'w'], optional): The mode in which to open the file. 
            'a' for append and 'w' for write. Defaults to 'a'.
    Returns:
        dict: A dictionary containing the result of the operation with the following keys:
            - 'SUCCESS' (bool): True if the operation was successful, False otherwise.
            - 'ERROR_MSG' (dict): A dictionary containing error messages if any errors occurred.
            - 'SUCCESS_MSG' (dict): A dictionary containing success messages.
            - 'RETURN' (Any): The return value, which is the error object if an error occurred.
    """


    function_result = {
        'SUCCESS': True,
        'ERROR_MSG': {},
        'SUCCESS_MSG': {},
        'RETURN': None
    }

    file_object = None

    try:
        file_object = open(file=path, mode=mode)
        file_object.writelines(data)
    except BaseException as error:
        function_result['SUCCESS'] = False
        function_result['ERROR_MSG']['file_error'] = f'{error}'
        function_result['RETURN'] = error
        return function_result
    else:
        return function_result
    finally:
        if file_object and not file_object.closed:
            file_object.close()

# endregion

# region read


def read_all(path) -> list[str]:
    """
    Reads all lines from a file at the given path.
    If the file does not exist, it attempts to create it and returns an empty list.
    If an error occurs during file operations, it captures the error message.
    Args:
        path (str): The path to the file to be read.
    Returns:
        dict: A dictionary containing:
            - 'SUCCESS' (bool): True if the operation was successful, False otherwise.
            - 'ERROR_MSG' (dict): A dictionary containing error messages, if any.
            - 'SUCCESS_MSG' (dict): A dictionary containing success messages, if any.
            - 'RETURN' (list[str] or Exception): The list of lines read from the file, or the exception if an error occurred.
    """


    function_result = {
        'SUCCESS': True,
        'ERROR_MSG': {},
        'SUCCESS_MSG': {},
        'RETURN': None
    }

    if not isfile(path=path):
        
        file_object = None
        try:
            file_object = open(file=path, mode='x')
            file_object.close()
        except BaseException as error:
            function_result['SUCCESS'] = False
            function_result['ERROR_MSG']['file_error'] = f'{error}'
            function_result['RETURN'] = error
            return function_result
        else:
            function_result['RETURN'] = []
            return function_result
        finally:
            if file_object and not file_object.closed:
                file_object.clos()

    file_object = None

    try:
        file_object = open(file=path, mode='r')
        function_result['RETURN'] = file_object.readlines()
    except BaseException as error:
        function_result['SUCCESS'] = False
        function_result['ERROR_MSG']['file_error'] = f'{error}'
        function_result['RETURN'] = error
        return function_result
    else:
        return function_result
    finally:
        if file_object and not file_object.closed:
            file_object.close()

# endregion
