from evaluation.models import Evaluation, Question

__all__ = ['create_evaluation', 'create_question', 'view_questions', 'view_evaluations', 'view_evaluation_by_lec',
           'create_questions_many']

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from users.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_evaluation(request):
    """
    Endpoint: /users/create_user/
    Method: POST
    Allowed users: All user
    Response status code: 201 created
    Description: admin can create users of a
    """

    #  if not request.user.has_perm('users.add_user'):
    #     return Response({'error': 'can not create user'}, status=status.HTTP_403_FORBIDDEN)


    evaluation_details = request.data
    lecturer = User.objects.get(id=evaluation_details['lec_id'])
    student = User.objects.get(id=evaluation_details['stud_id'])


    eval = Evaluation(
        lecturer_id=lecturer,
        student_id=student,

    )
    eval.save()
    eval_details = {}
    eval_details['evaluation_id'] = eval.id

    # return Response({'success': "user added successfully"}, status=status.HTTP_201_CREATED)
    return Response(eval_details, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_question(request):
    """
    Endpoint: /users/create_user/
    Method: POST
    Allowed users: All user
    Response status code: 201 created
    Description: admin can create users of a
    """

    #  if not request.user.has_perm('users.add_user'):
    #     return Response({'error': 'can not create user'}, status=status.HTTP_403_FORBIDDEN)


    question_details = request.data
    evaluation = Evaluation.objects.get(id=question_details['evaluation_id'])

    que = Question(
        question=question_details['question'],
        category=question_details['category'],
        evaluation_id=evaluation,
        rating=question_details['rating']

    )
    que.save()

    return Response({'success': "question added successfully"}, status=status.HTTP_201_CREATED)
    # return Response(eval_details, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_questions_many(request):
    """
    Endpoint: /users/create_user/
    Method: POST
    Allowed users: All user
    Response status code: 201 created
    Description: admin can create users of a
    """

    #  if not request.user.has_perm('users.add_user'):
    #     return Response({'error': 'can not create user'}, status=status.HTTP_403_FORBIDDEN)
    question_details = request.data
    for que_details in question_details:
        evaluation = Evaluation.objects.get(id=question_details['evaluation_id'])
        que = Question(
            question=que_details['question'],
            category=que_details['category'],
            evaluation_id=evaluation,
            rating=que_details['rating']

        )
        que.save()

    return Response({'success': "questions added successfully"}, status=status.HTTP_201_CREATED)
    # return Response(eval_details, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def view_questions(request):
    """
    Endpoint: /user/view_questions/<status>/
    Method: GET
    Allowed users: Admins
    Response status code: 200 success
    Description: Admins can view all users created
    """
    # if not request.user.has_perm('users.can_view_users'):
    #    return Response({'error': "can not view users"}, status=status.HTTP_403_FORBIDDEN)


    que = Question.objects.all()
    if not que:
        return Response([])

    data = []
    for question in que:
        question_details = {}
        question_details['question'] = question.question
        question_details['category'] = question.category
        question_details['evaluation_id'] = question.eval_id()
        question_details['rating'] = question.rating

        data.append(question_details)

    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def view_evaluations(request):
    """
    Endpoint: /user/view_questions/<status>/
     Method: GET
    Allowed users: Admins
    Response status code: 200 success
    Description: Admins can view all users created
    """
    # if not request.user.has_perm('users.can_view_users'):
    #    return Response({'error': "can not view users"}, status=status.HTTP_403_FORBIDDEN)


    eval = Evaluation.objects.all()
    if not eval:
        return Response([])

    data = []
    for evaluation in eval:
        evaluation_details = {}
        evaluation_details['evaluation_id'] = evaluation.id
        #evaluation_details['lecturer_id'] = evaluation.lecturer_id
        evaluation_details['lecturer_id'] = evaluation.lec_id()
        evaluation_details['student_id'] = evaluation.stud_id()

        data.append(evaluation_details)

    return Response(data)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def view_evaluation_by_lec(request, lec):
    """
    Endpoint: /evaluation/view_evaluations/<lec>/
    Method: GET
    Allowed users: All users
    Response status code: 200 success
    Description: Used to check if activation key is in the DB 
    """
    try:
        evals = Evaluation.objects.filter(lecturer_id=lec)
        data = []
        question_details = {}
        evaluation_details = {}
        for evaluation in evals:

            evaluation_details['evaluation_id'] = evaluation.id
            evaluation_details['lecturer_id'] = evaluation.lec_id()
            evaluation_details['student_id'] = evaluation.stud_id()
            que = Question.objects.filter(evaluation_id=evaluation.id)
            que_data = []

            for question in que:

                question_details['question'] = question.question
                question_details['category'] = question.category
                question_details['evaluation_id'] = question.evaluation_id
                question_details['rating'] = question.rating

                que_data.append(question_details)
            evaluation_details['questions'] = que_data

        data.append(evaluation_details)

        return Response(data)
    except ObjectDoesNotExist:
        return Response({'error': "not found"}, status=status.HTTP_404_NOT_FOUND)
