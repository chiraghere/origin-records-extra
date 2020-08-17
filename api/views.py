from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, PersonSerializer, RelationSerializer
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Person, Relation

class UserCreate(APIView):
    """
    Creates a new user.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Userlogin(APIView):

    def post(self, request, format='json'):
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user:
            token = Token.objects.get(user=user)
            json = {'token': token.key}
            return Response(json, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class PersonView(APIView):
    """
    Get all the existing nodes of a user and create new nodes
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        queryset = Person.objects.filter(created_by=request.user)
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format='json'):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RelationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Relation.objects.all()
        serializer = RelationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        new_person = PersonSerializer(data=data[0])
        if new_person.is_valid():
            new_person.validated_data['created_by'] = request.user
            new_person.save()

        person_set = Person.objects.all()
        person = person_set[len(person_set)-1]
        data[1]['relation_from'] = person.id

        if data[1]['relation'] == 'child':
            temp = data[1]['relation_from']
            data[1]['relation_from'] = data[1]['relation_to']
            data[1]['relation_to'] = temp
            data[1]['relation'] = 'parent'

        serializer = RelationSerializer(data=data[1])
        if serializer.is_valid():
            serializer.validated_data['created_by'] = request.user
            serializer.save()

            relation_from = Person.objects.get(id=data[1]['relation_from'])
            relation_to = Person.objects.get(id=data[1]['relation_to'])
            relation = serializer.validated_data['relation']

            if relation == 'parent':
                Partner_set = Relation.objects.filter(relation_from=relation_from, relation='partner')
                if len(Partner_set) != 0:
                    for Partner in Partner_set:
                        x = Relation.objects.create(relation_from=Partner.relation_to, relation_to=relation_to,
                                                          relation='parent', created_by=request.user)
                        x.save()

            elif relation == 'partner':
                Partner_set = Relation.objects.filter(relation_from=relation_to, relation='partner')
                if len(Partner_set) == 0:
                    x = Relation.objects.create(relation_from=relation_to, relation_to=relation_from,
                                                      relation='partner', created_by=request.user)
                    x.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
