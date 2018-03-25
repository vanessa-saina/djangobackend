from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist

import json
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from utilities.dict import *
# Create your views here.
HEADERS = {
	'accept': 'application/json',
	'content-type': 'application/json'
}


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_dict(request):
    """
    Endpoint: /dict/get_dict/
    Method: GET
    Allowed users: All
    Response status code: 200 success
    Description: View the rearranged dict
    """
    data = get_mydict()
    response_data = data

    return Response(response_data, status=status.HTTP_200_OK)
