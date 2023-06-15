from django.shortcuts import render
from core.models import Course
from core.serializers import CourseSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
# Create your views here.

class CourseList(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    def post(self, request):

        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.error, status=400)
    

class CourseDetail(APIView):

    def get_object(self, pk):
        try:
            courseDetails = Course.objects.get(id = pk)
            return courseDetails
        except Course.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        CourseDetails = self.get_object(pk)
        serializer = CourseSerializer(CourseDetails)
        return Response(serializer.data)
    
    def put(self, request, pk):
        CourseDetails = self.get_object(pk)
        serializer = CourseSerializer(CourseDetails, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.error, status=400)
    
    def delete(self, request, pk):
        CourseDetails = self.get_object(pk)
        CourseDetails.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)