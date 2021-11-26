from django.contrib.auth.hashers import check_password
from django.contrib.auth import login

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import RegistrationSerializer
from .models import User
from .utils import course_year_extractor
from courses.models import *
from neo4j import *

@api_view(['POST'])
def student_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['response'] = 'Student registered successfully'
        data['id'] = user.id
        data['reg_number'] = user.reg_number
        data['email'] = user.email
        data['full_name'] = user.full_name
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
def lecturer_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['response'] = 'Lecturer registered successfully'
        data['id'] = user.id
        data['staff_id'] = user.staff_id
        data['email'] = user.email
        data['full_name'] = user.full_name
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
def login(request):
    data = {}
    email = request.data['email']
    password = request.data['password']

    # check if account exists
    try:
        user = User.objects.get(email=email)
    except BaseException as erorr:
        raise ValidationError(
            {'400': '{}'.format(erorr)}
        )

    # get or create new token
    token = str(Token.objects.get_or_create(user=user)[0])
    data['token'] = token

    # check if password is corresct
    if not check_password(password, user.password):
        raise ValidationError(
            {'message': 'Incorrect credentials'}
        )

    if user:
        data['response'] = 'User logged in successfully'
        data['id'] = user.id
        data['email'] = user.email
        data['full_name'] = user.full_name
        return Response(data)
    else:
        raise ValidationError(
            {'400': 'Account doesnt exist'}
        )
