from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from py2neo import NodeMatcher

from users.models import User
from .models import *
from .serializers import *

from neo4j import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, ])
def add_fuculty(request):
    user = request.user
    serializer = FucultySerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        fuculty = serializer.save()
        data['name'] = fuculty['name']
        data['dean'] = fuculty['dean']
    else:
        data = serializer.errors
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, ])
def add_school(request):
    serializer = SchoolSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        school = serializer.save()
        data['name'] = school['name']
        data['director'] = school['director']
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def add_unit(request):
    serializer = UnitSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        unit = serializer.save()
        data['name'] = unit['name']
        data['code'] = unit['code']
        data['course'] = unit['course']
    else:
        data = serializer.errors
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_all_students(request):
    data = {}
    node_matcher = NodeMatcher(graph)
    students = node_matcher.match('StudentNode')
    stdnts = []
    for student in students:
        stdnts.append(list(student.items())[0][1] + ' : ' + list(student.items())[1][1])
    data['students'] = stdnts
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_all_units(request):
    data = {}
    node_matcher = NodeMatcher(graph)
    units = node_matcher.match('UnitNode')
    unts = []
    for unit in units:
        unts.append(list(unit.items())[1][1] + ' : ' + list(unit.items())[0][1])
    data['units'] = unts
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_all_lecturers(request):
    data = {}
    node_matcher = NodeMatcher(graph)
    lecturers = node_matcher.match('LecturerNode')
    lcs = []
    for lec in lecturers:
        lcs.append(list(lec.items())[1][1] + ' : ' + list(lec.items())[0][1])
    data['lecturers'] = lcs
    return Response(data)
