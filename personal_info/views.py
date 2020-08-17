from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import *
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api.models import *
# Create your views here.


class Show_Relations(APIView):

    def get(self, request):
        final = {}
        Person_set = Person.objects.filter(created_by=request.user)
        serializer_person = PersonSerializer(Person_set, many=True)

        Relation_set = Relation.objects.filter(created_by=request.user)
        serializer_relation = RelationSerializer(Relation_set, many=True)

        final['Person_set'] = serializer_person.data
        final['Relation_set'] = serializer_relation.data

        return JsonResponse(final)

    def post(self, request):
        data = JSONParser().parse(request)
        Result = {}
        person = Person.objects.get(id=data['id'], created_by=request.user)
        Result['Me'] = person.id
        Relation_set = Relation.objects.filter(relation_from=person, created_by=person.created_by)
        Result['child'] = []

        for i in Relation_set:
            if i.relation == 'parent':
                Result['child'].append(i.relation_to.id)
            elif i.relation == 'partner':
                Result['partner'] = i.relation_to.id

        Relation_set = Relation.objects.filter(relation_to=person, created_by=person.created_by)

        for i in Relation_set:
            if i.relation == 'parent':
                if i.relation_from.gender == 'Male':
                    Result['father'] = i.relation_from.id
                elif i.relation_from.gender == 'Female':
                    Result['mother'] = i.relation_from.id

        return JsonResponse(Result)


class Search(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        persons = Person.objects.all()
        if 'id' in request.GET:
            personid = request.GET['id']
            persons = persons.filter(id=personid)
        if 'lastname' in request.GET:
            last_name = request.GET['lastname']
            persons = persons.filter(last_name=last_name)
        if 'firstname' in request.GET:
            first_name = request.GET['firstname']
            persons = persons.filter(first_name=first_name)
        if 'birthplace' in request.GET:
            birthplace = request.GET['birthplace']
            persons = persons.filter(birthplace=birthplace)
        
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)