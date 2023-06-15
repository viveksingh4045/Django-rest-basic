from rest_framework import serializers
from core.models import Student

#Serializers are used to convert Query Objects to JSON and JSON to query Objects
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__' #for specific columns only use-> fields = ['colName1', 'colName2']
