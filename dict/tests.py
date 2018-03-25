from django.test import TestCase

# Create your tests here.
a = {'34': 'thirty-four', '90': 'ninety',
'91': 'ninety-one','21': 'twenty-one',
'61': 'sixty-one', '9': 'nine',
'2': 'two', '6': 'six', '3': 'three',
'8': 'eight', '80': 'eighty', '81': 'eighty-one',
'Ninety-Nine': '99', 'nine-hundred': '900',}


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
print sorted(a.items(), key=lambda t: get_key(t[0]))