"""
This module carries all the functions that are not http handlers which are used in the user's views module.
"""


__all__ = ['create_token', 'check_if_email_exists', 'assign_permissions']

import jwt

from rest_framework_jwt.utils import jwt_payload_handler

from development import settings

from users.models import User

def create_token(user):
	"""
	creates a token that is used to authenticate a user with every request.
	returns the token
	user
	"""
	payload = jwt_payload_handler(user)
	token = jwt.encode(payload, settings.SECRET_KEY)
	return token.decode("unicode_escape")


def check_if_email_exists(email):
	"""
	checks if email exists when creating a new user.
	returns true if user exists, else False
	email: email that is being cheked.
	"""
	users = User.objects.all()

	for user in users:
		if user.email == email:
			return True
			
	return False

def assign_permissions(sysem_permissions, user_permissions, user):
	"""
	assigns permissions to a newly created user

	system_permissions: all system permissions
	user_permissions: all the permissions selected for a particular user
	user: user to assign permissions to. 
	"""
	permissions_to_grant_user = []
	for system_perm in sysem_permissions:
		for user_perm in user_permissions:
			if system_perm.codename == user_perm:
				permissions_to_grant_user.append(system_perm.id)		
	
	user.user_permissions.set(permissions_to_grant_user)