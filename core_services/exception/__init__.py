from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
import traceback
from django.conf import settings
import sys
from ..logs import  log
# from .log_util import log

def handle_exception(exc, context=None):
    """
    Global exception handler for DRF views.

    Parameters:
    - exc: The exception instance
    - context: Optional DRF context (like request info)

    Returns:
    - Response: DRF Response object with error details
    """

    # Handle DRF API exceptions (ValidationError, NotFound, etc.)
    log.error(exc)
    if isinstance(exc, APIException):
        return Response(
            {
                "status": False,
                "error": exc.detail if hasattr(exc, "detail") else str(exc),
                "type": exc.__class__.__name__,
            },
            status=getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST),
        )

    # Generic Python exceptions
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print(tb, file=sys.stderr)  # Optional: log to stderr or a file

    return Response(
        {
            "status": False,
            "error": str(exc),
            "type": exc.__class__.__name__,
            "traceback": tb if settings.DEBUG else "Hidden in production",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
