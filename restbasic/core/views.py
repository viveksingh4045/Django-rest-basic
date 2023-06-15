from django.shortcuts import render
from django.http import HttpResponse
from core.models import Student
from core.serializers import StudentSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET','POST'])
def student(request):

    if request.method == "GET":
        studentList = Student.objects.all()
        serializer = StudentSerializer(studentList, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        print(request.data)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


def students(request,pk):

    if request.method == "GET":
        studentList = Student.objects.get(id = pk)
        print(studentList.__dict__)
        serializer = StudentSerializer(studentList)
        return HttpResponse({'StudentDet':serializer.data})
    
    elif request.method == "POST":
        print(request.data)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

