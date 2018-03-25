"""
This module carries all the functions that are not http handlers which are used in the user's views module.
"""


__all__ = ['get_mydict']

import jwt

from rest_framework_jwt.utils import jwt_payload_handler

from development import settings

from users.models import User

dict = {'34': 'thirty-four', '90': 'ninety',
'91': 'ninety-one','21': 'twenty-one',
'61': 'sixty-one', '9': 'nine',
'2': 'two', '6': 'six', '3': 'three',
'8': 'eight', '80': 'eighty', '81': 'eighty-one',
'Ninety-Nine': '99', 'nine-hundred': '900'}


"""
Compares int value for sorting.

:param x: key 
:returns: -1 or 1 
:raises keyError: raises an exception if not int value
"""
def get_key(key):
    #checks if int
    try:
        return int(key)
    except ValueError:
        return key



def get_mydict():
	#print sorted(dict.items(), key=lambda t: get_key(t[0]))
	myDict =  sorted(dict.items(), key=lambda t: get_key(t[0]))

	return myDict