from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
import pprint
import inspect
import os


class DebugDie(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Debug dump"
    default_code = "debug_die"


def dd(*args):
    """
    Laravel-style dump and die for Django REST Framework.
    Accepts multiple arguments and prints them inside {} with debug info.
    """
    # Get caller info
    frame = inspect.stack()[1]
    file_path = frame.filename
    line_no = frame.lineno
    func_name = frame.function
    short_path = os.path.relpath(file_path, os.getcwd())

    # Build a dictionary of arguments for display
    data = {f"arg_{i+1}": arg for i, arg in enumerate(args)}

    # Print info in terminal
    print("\n" + "="*80)
    print(f"🧠 DEBUG DIE at {short_path}:{line_no} (function: {func_name})")
    print("="*80)
    pprint.pprint(data)
    print("="*80 + "\n")

    # Build response payload for API
    response_data = {
        "debug": data,
        "location": {
            "file": short_path,
            "line": line_no,
            "function": func_name,
        }
    }

    # Stop execution immediately
    raise DebugDie(detail=response_data)