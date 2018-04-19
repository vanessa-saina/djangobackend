__all__ = ['login', 'create_user', 'view_users', 'approve_users', 'delete_user',
            'check_activation_key', 'update_account', 'search_users', 'view_lecturers']

import string

from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from utilities.user import *

from .models import User, Myunit

USER_CREATION_MESSAGE =  "Dear %s, You have just been registered on the Lecturer Evaluation platform with " \
                    "reg_number %s and password %s. " \
                    "To access the platform, follow this http://localhost:4000/#!/activate-account/%s " \
                    "to activate account and change your password. " \
                    "Regards, Quality Assuarance team"


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    """
    Endpoint: /users/userlogin/
    Method: POST
    Allowed users: All users
    Response status code: 200 success
    Description: Logs in a user
    """
    try:
    	reg_number = request.data['username']
    	password = request.data['password']
    except KeyError:
    	return Response({'error': 'please enter username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=reg_number, password=password)

    if user:
        authenticaction_token = create_token(user)
        user_details = {}
        user_details['name'] = "%s %s" %  (user.first_name, user.last_name)

        user_details['token'] = authenticaction_token
        user_details['role'] = user.role
        user_details['id'] = user.id

        # update the last login section
        user_logged_in.send(sender=user.__class__, request=request, user=user)

        return Response(user_details, status=status.HTTP_200_OK)
    else:
        response = {'error': "can not authenticate with the given credentials or account has been deactivated"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_user(request):
    """
    Endpoint: /users/create_user/
    Method: POST
    Allowed users: All user
    Response status code: 201 created
    Description: admin can create users of a
    """

  #  if not request.user.has_perm('users.add_user'):
   #     return Response({'error': 'can not create user'}, status=status.HTTP_403_FORBIDDEN)

    if check_if_email_exists(request.data['email']):
        return Response({'error': "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user_details = request.data
    user = User(
        email=user_details['email'],
        first_name=user_details['first_name'],
        last_name=user_details['last_name'],
        role=user_details['role'],
        status=200,
        is_active=True,
        is_staff=False,
        password=make_password(user_details['password'])
    )

    user.save()

    permissions = Permission.objects.all()
    assign_permissions(permissions, user_details['permissions'], user)

    return Response({'success': "user added successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def view_users(request):
    """
    Endpoint: /user/view_users/<status>/
    Method: GET
    Allowed users: Admins
    Response status code: 200 success
    Description: Admins can view all users created
    """
   # if not request.user.has_perm('users.can_view_users'):
    #    return Response({'error': "can not view users"}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.all()
    if not users:
        return Response([])

    data = []
    for user in users:
        user_details = {}
        user_details['name'] = "%s %s" % (user.first_name, user.last_name)
        user_details['status'] = user.is_active
        user_details['date_created'] = user.date_joined
        user_details['last_login'] = user.last_login
        user_details['email'] = user.email
        user_details['role'] = user.role
        user_details['id'] = user.id
        user_details['staff'] = user.is_staff

        data.append(user_details)

    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def view_lecturers(request):
    """
    Endpoint: /user/view_users/<status>/
    Method: GET
    Allowed users: Admins
    Response status code: 200 success
    Description: Admins can view all users created
    """
   # if not request.user.has_perm('users.can_view_users'):
    #    return Response({'error': "can not view users"}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.filter(role='lecturer')
    if not users:
        return Response([])

    data = []
    for user in users:
        user_details = {}
        user_details['name'] = "%s %s" % (user.first_name, user.last_name)
        user_details['status'] = user.is_active
        user_details['date_created'] = user.date_joined
        user_details['last_login'] = user.last_login
        user_details['email'] = user.email
        user_details['role'] = user.role
        user_details['id'] = user.id
        user_details['staff'] = user.is_staff
     #   user_details['units'] = Myunit.objects.filter(id=user.id)

        data.append(user_details)

    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def search_users(request, name):
    """
    Endpoint: /user/search_users/<name>/
    Method: GET
    Allowed users: Admins
    Response status code: 200 success
    Description: Admins can view all users created. They view them by name.
    - users not approved yet, users that have been approved, and users that have been rejected
    """



    account_name = name
    users = User.objects.filter(Q(first_name__icontains=account_name)|Q(last_name__icontains=account_name)).exclude(id=request.user.id)
    if not users:
        return Response([])

    data = []
    for user in users:
        user_details = {}
        user_details['name'] = "%s %s" % (user.first_name, user.last_name)
        user_details['status'] = user.is_active
        user_details['date_created'] = user.date_joined
        user_details['last_login'] = user.last_login
        user_details['email'] = user.email
        user_details['role'] = user.role
        user_details['id'] = user.id

        data.append(user_details)

    return Response(data)

@api_view(['PUT'])
def approve_users(request):
    """
    Endpoint: /user/approve_users/
    Method: PUT
    Allowed users: Admins
    Response status code: 200 success
    Description: Admin can approve users.
    - After approval, an email is sent to the user
    """
    if not request.user.has_perm('users.can_approve_users'):
        return Response({'error': "can not approve users"}, status=status.HTTP_403_FORBIDDEN)

    user_ids = request.data['user_ids']

    for id in user_ids:
        user = User.objects.get(id=id)

        user.status = 200
        password = code()
        user.password = make_password(password)
        user.save()
        message_data = {
            'subject': "Account creation",
            'content': USER_CREATION_MESSAGE % (user.first_name, user.email, password),
            'phone': user.phone,
            'email': user.email,
            'channel': "EMAIL",
        }

    #    send_message(message_data)

    return Response({'success': "users successfully approved"})


@api_view(['DELETE'])
def delete_user(request, user_id):
    """
    Endpoint: /users/delete_user/<user_id>/
    Method: Delete
    Allowed users: Admins
    Response status code: 204
    Description: This view deletes a user
    """
    user = User.objects.get(id=user_id)

    user.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def check_activation_key(request, key):
    """
    Endpoint: /users/check_activation_key/<key>/
    Method: GET
    Allowed users: All users
    Response status code: 200 success
    Description: Used to check if activation key is in the DB 
    """
    try:
        user = User.objects.get(phone_activation_code=key)
        data = {
            "name": "%s %s" % (user.first_name, user.last_name),
            "key": user.phone_activation_code
        }
        return Response(data)
    except ObjectDoesNotExist:
        return Response({'error': "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes((AllowAny, ))
def update_account(request):
    """
    Endpoint: /users/update_account/
    Method: PUT
    Allowed users: Users registered by the system
    Response status code: 200 success
    Description: Created users can update account then change password here
    """
    old_password = request.data['old_password']
    new_password = request.data['new_password']
    user_id = request.data['id']

    try:
        user = User.objects.get(user_id)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.is_active = True
        #    user.phone_activation_code="activated"
            user.save()
            return Response({'success': "password changed successfully"})
        else:
            return Response({'error': "incorrect wrong password"}, status=status.HTTP_403_FORBIDDEN)
    except ObjectDoesNotExist:
        return Response({'error': "key not found"})