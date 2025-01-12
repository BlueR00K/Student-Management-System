from DL.mini_dl import write_line, write_list, read_all
from typing import Hashable, Any
from common.utility import search
from datetime import date

# region Select Data Source
source_path = r'DB\data_source.txt'
backup_path = r'DB\backup.txt'
# endregion


# region converters


def dictlist_to_strlist(st_list: list[dict]) -> map:
    """
    Converts a list of dictionaries to a map of formatted strings.
    Args:
        st_list (list[dict]): A list of dictionaries where each dictionary represents a student.
    Returns:
        map: A map object where each element is a formatted string representation of a dictionary, followed by a newline character.
    """
    

    return map(lambda student: f'{student}\n', st_list)


def strlist_to_dictlist(st_list: list[str]) -> map:
    """
    Converts a list of strings to a map of dictionaries.
    Each string in the input list is expected to represent a dictionary in string format.
    The function strips any leading or trailing whitespace from each string and then
    evaluates it to convert it into a dictionary.
    Args:
        st_list (list[str]): A list of strings, where each string represents a dictionary.
    Returns:
        map: A map object containing dictionaries converted from the input strings.
    Raises:
        SyntaxError: If any string in the list is not a valid dictionary representation.
        TypeError: If the input is not a list of strings.
    """
    

    return map(lambda student: eval(student.strip()), st_list)

# endregion

# region validation


def age(birth_year):
    today = date.today()
    age = today.year - int(birth_year)
    return age


def _isvalid(student: dict, mode = 'add'):
    """
    Validates the student dictionary based on various criteria.
    Args:
        student (dict): A dictionary containing student information with keys 'name', 'family', 'gender', 'stcode', 'ncode', and 'birth'.
        mode (str, optional): The mode of operation, either 'add' or another mode. Defaults to 'add'.
    Returns:
        dict: A dictionary containing the validation result with keys:
            - 'SUCCESS' (bool): True if validation is successful, False otherwise.
            - 'ERR_MSG' (dict): A dictionary containing error messages for each invalid field.
            - 'SUC_MSG' (dict): A dictionary containing success messages (currently unused).
            - 'RETURN' (None): Placeholder for additional return data (currently unused).
    Validation Criteria:
        - 'name': Must not be empty and must contain only alphabetic characters.
        - 'family': Must not be empty and must contain only alphabetic characters.
        - 'gender': Must not be empty and must be one of 'male', 'female', or 'other'.
        - 'stcode': Must not be empty, must be 12 digits long, and must contain only digits.
        - 'ncode': Must not be empty, must be 11 digits long, and must contain only digits.
        - 'birth': Must not be empty, must represent an age between 8 and 120, and must contain only digits.
    Additional Checks (for 'add' mode):
        - Ensures 'stcode' and 'ncode' are unique by checking existing records.
    """
    

    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    if not student['name']:
        function_result['ERR_MSG']['name'] = 'Name column is empty'
    elif not student['name'].isalpha():
        function_result['ERR_MSG']['name'] = 'Name is not alphabet'

    if not student['family']:
        function_result['ERR_MSG']['family'] = 'Family column is empty'
    elif not student['family'].isalpha():
        function_result['ERR_MSG']['family'] = 'Famlily is not alphabet'

    if not student['gender']:
        function_result['ERR_MSG']['gender'] = 'Gender is empty'
    elif student['gender'] not in ('male', 'female', 'other'):
        function_result['ERR_MSG']['gender'] = 'unvalid gender'

    if not student['stcode']:
        function_result['ERR_MSG']['stcode'] = 'Student Code is empty'
    elif len(student['stcode']) != 12:
        function_result['ERR_MSG']['stcode'] = 'Student Code must be 12 digits'
    if not student['stcode'].isdecimal():
        function_result['ERR_MSG']['stcode'] = 'Student Code must contain digits only'

    if not student['ncode']:
        function_result['ERR_MSG']['ncode'] = 'National Code is empty'
    elif len(student['ncode']) != 11:
        function_result['ERR_MSG']['ncode'] = 'Nantionl Code must be 11 digits'
    elif not student['ncode'].isdecimal():
        function_result['ERR_MSG']['ncode'] = 'National Code must contain digits only'

    if not student['birth']:
        function_result['ERR_MSG']['birth'] = 'Birth is empty'
    elif age(student['birth']) not in range(8, 120):
        function_result['ERR_MSG'][
            'birth'] = 'Age is not in valid range\n(must be between 8 and 120)'
    elif not student['birth'].isdecimal():
        function_result['ERR_MSG']['birth'] = 'Birth must contain digits only'

    if function_result['ERR_MSG']:
        function_result['SUCCESS'] = False

    if mode == 'add':
        for std in get_data('stcode', 'ncode')['RETURN']:
            if std:
                if student['stcode'] == std['stcode']:
                    function_result['SUCCESS'] = False
                    function_result['ERR_MSG']['STCODE'] = f'{std["stcode"]} exists'
                
                if student['ncode'] == std['ncode']:
                    function_result['SUCCESS'] = False
                    function_result['ERR_MSG']['NCODE'] = f'{std["ncode"]} exists'
                
                print(f'\n{mode} : {function_result["SUCCESS"]} : {std}')

    return function_result

# endregion

# region create student

def create_std(student: dict[str, str]) -> dict[str, Any]:
    """
    Creates a student record.
    Args:
        student (dict[str, str]): A dictionary containing student information.
    Returns:
        dict[str, Any]: A dictionary containing the result of the operation with keys:
            - 'SUCCESS' (bool): Indicates if the operation was successful.
            - 'ERR_MSG' (dict): Contains error messages if any errors occurred.
            - 'SUC_MSG' (dict): Contains success messages if the operation was successful.
            - 'RETURN' (None): Reserved for future use, currently always None.
    """
    

    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    result = _isvalid(student)

    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG'] = result['ERR_MSG']
        return function_result

    result = write_line(source_path, f'{student}\n')

    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['FILE_ERROR'] = 'Source Error'
    else:
        function_result['SUC_MSG'] = 'Successfully added'

    return function_result

# endregion

# region extract data from dl


def get_data(*columns) -> dict[Any]:
    """
    Fetches data from a source file and returns it as a dictionary.
    Args:
        *columns: Variable length argument list specifying the columns to be included in the result.
    Returns:
        dict[Any]: A dictionary containing the following keys:
            - 'SUCCESS' (bool): Indicates if the operation was successful.
            - 'ERR_MSG' (dict): Contains error messages if any.
            - 'SUC_MSG' (dict): Contains success messages if any.
            - 'RETURN' (list or None): The fetched data as a list of dictionaries if successful, otherwise None.
    Raises:
        KeyError: If a specified column does not exist in the data.
    """
    

    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    print(source_path)
    result = read_all(path=source_path)

    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG'] = 'Source Error'
        return function_result

    result = list(strlist_to_dictlist(result['RETURN']))


    if not columns:
        function_result['RETURN'] = result
    else:
        function_result['RETURN'] = list(
            map(
                lambda student: {column: student[column] for column in columns}, result
            )
        )

    return function_result

# endregion

# region edit student


def edit_std(student: dict[str, Any]) -> dict[str, Any]:
    """
    Edits the details of a student in the student list.
    Args:
        student (dict[str, Any]): A dictionary containing the student's details to be edited. 
            The dictionary must include the keys 'stcode', 'ncode', 'name', 'family', 'gender', and 'birth'.
    Returns:
        dict[str, Any]: A dictionary containing the result of the operation with the following keys:
            - 'SUCCESS' (bool): Indicates whether the operation was successful.
            - 'ERR_MSG' (dict): Contains error messages if the operation failed.
            - 'SUC_MSG' (str): Contains a success message if the operation was successful.
            - 'RETURN' (None): Reserved for future use.
    The function performs the following steps:
    1. Validates the input student data.
    2. Retrieves the current student list.
    3. Searches for the student in the list by 'stcode' or 'ncode'.
    4. Updates the student's details if found.
    5. Writes the updated student list back to the source.
    6. Returns the result of the operation.
    """
    

    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    result = _isvalid(student, mode='edit')
    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG'] = result['ERR_MSG']
        return function_result

    result = get_data()
    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['FILE_ERROR'] = 'Source Error'
        return function_result

    student_list = list(result['RETURN'])

    for std in student_list:
        if student['stcode'] == std['stcode'] or \
                student['ncode'] == std['ncode']:
            std['name'] = student['name']
            std['family'] = student['family']
            std['gender'] = student['gender']
            std['birth'] = student['birth']
            break
    else:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['ID_ERROR'] = 'The desired student was\'nt found'
        return function_result

    result = write_list(
        path=source_path, data=dictlist_to_strlist(student_list), mode='w')

    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['FILE_ERROR'] = 'Source Error'
        return function_result

    function_result['SUC_MSG'] = (
        f'Student successfully edited\nstcode: {student["stcode"]}\nncode: {student["ncode"]}')

    return function_result

    # endregion

# region delete student


def delete_std(student: dict[str, Any]) -> dict[str, Any]:
    """
    Deletes a student from the student list.
    Args:
        student (dict[str, Any]): A dictionary containing student information with keys 'stcode' and 'ncode'.
    Returns:
        dict[str, Any]: A dictionary containing the result of the operation with keys:
            - 'SUCCESS' (bool): Indicates if the operation was successful.
            - 'ERR_MSG' (dict): Contains error messages if any errors occurred.
            - 'SUC_MSG' (str): Success message if the operation was successful.
            - 'RETURN' (None): Placeholder for return value, always None in this function.
    Raises:
        KeyError: If the student dictionary does not contain the required keys.
    """


    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    result = _isvalid(student=student, mode = 'delete')
    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG'] = result['ERR_MSG']
        return function_result

    result = get_data()
    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['FILE_ERROR'] = 'Source Error'
        return function_result

    student_list = list(result['RETURN'])

    for std in student_list:
        if student['stcode'] == std['stcode']:
            student_list.remove(std)
            break
    else:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['ID_ERROR'] = 'The desired student was\'nt found'
        return function_result

    result = write_list(
        path=source_path, data=dictlist_to_strlist(student_list), mode='w')

    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['FILE_ERROR'] = 'Source Error'
        return function_result

    function_result['SUC_MSG'] = (
        f'Student successfully deleted\nstcode: {student["stcode"]}\nncode: {student["ncode"]}'
    )
    return function_result
# endregion

# region search student

def search_std(key: Hashable, value: Any) -> dict[str, Any]:
    """
    Search for a specific key-value pair in a data source.
    Args:
        key (Hashable): The key to search for in the data.
        value (Any): The value associated with the key to search for.
    Returns:
        dict[str, Any]: A dictionary containing the search results with the following keys:
            - 'SUCCESS' (bool): Indicates if the search was successful.
            - 'ERR_MSG' (dict): Contains error messages if any occurred.
            - 'SUC_MSG' (dict): Contains success messages if any occurred.
            - 'RETURN' (Any): The search result if successful, otherwise None.
    """


    function_result = {
        'SUCCESS': True,
        'ERR_MSG': {},
        'SUC_MSG': {},
        'RETURN': None
    }

    result = get_data()
    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG']['FILE_ERROR'] = 'Source Error'
        return function_result

    result = search(data_list=result['RETURN'], key=key, value=value)
    if not result['SUCCESS']:
        function_result['SUCCESS'] = False
        function_result['ERR_MSG'] = result['ERR_MSG']
        return function_result
    
    function_result['RETURN'] = result['RETURN']
    return function_result
# endregion

# region Source File

# Function to create a backup of the current database
def create_backup(backup_path: str = backup_path) -> dict:
    """
    Creates a backup of a source file to the specified backup path.
    Args:
        backup_path (str): The path where the backup file will be created.
    Returns:
        dict: A dictionary containing the result of the backup operation.
            - 'SUCCESS' (bool): True if the backup was created successfully, False otherwise.
            - 'ERR_MSG' (str, optional): The error message if an exception occurred during the backup process.
    Raises:
        Exception: If an error occurs during reading from the source file or writing to the backup file.
    """

    try:
        with open(source_path, 'r') as src_file:
            data = src_file.read()
        with open(backup_path, 'w') as backup_file:
            backup_file.write(data)
        return {'SUCCESS': True}
    except Exception as e:
        return {'SUCCESS': False, 'ERR_MSG': str(e)}

# Function to clear the current database (clear data)
def clear_database() -> dict:
    """
    Clears the database by overwriting the file at the specified source path with headers.
    This function attempts to open the file located at `source_path` in write mode and writes
    a predefined header string to it. If the operation is successful, it returns a dictionary
    indicating success. If an exception occurs during the file operation, it catches the 
    exception and returns a dictionary indicating failure along with the error message.
    Returns:
        dict: A dictionary with the following keys:
            - 'SUCCESS' (bool): True if the operation was successful, False otherwise.
            - 'ERR_MSG' (str, optional): The error message if an exception occurred.
    Raises:
        Exception: Any exception that occurs during the file operation is caught and its
        message is included in the returned dictionary under the 'ERR_MSG' key.
    """

    try:
        headers = "name|family|gender|birth|ncode|stcode\n"
        with open(source_path, 'w') as file:
            file.write(headers)
        return {'SUCCESS': True}
    except Exception as e:
        return {'SUCCESS': False, 'ERR_MSG': str(e)}

# endregion