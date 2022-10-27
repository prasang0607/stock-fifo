from django.utils.encoding import force_str
from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    # status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code=500):
        # if status_code is not None:
        self.status_code = status_code

        if detail:
            d = force_str(detail)
        else:
            d = self.default_detail

        self.detail = d
