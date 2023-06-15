from azure.storage.blob import BlobServiceClient
from core.models import Employee
from core.customuserpermission import BatchUploadDownloadPermission
from core.serializers import EmployeeSerializer
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group, User, Permission
import pandas as pd
import re
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from io import BytesIO

# Create your views here.
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([BatchUploadDownloadPermission])
def batchjob(request):
    """
    This API support bulk data insert operation to SQL server Employee table.
    It supports file types Excel and CSV.
    Column names should be Emp_ID, Name, Age, Phone_No, Address, DOJ
    """
    if request.method == "GET":
        
        EmployeeList = Employee.objects.all().values()
        df = pd.DataFrame.from_records(EmployeeList)
        file = BytesIO()
        df.to_excel(file, index=False)
        file.seek(0)
        response = HttpResponse(file.getvalue(),\
                                 content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',\
                                )
        response['Content-Disposition'] = 'attachment; filename="my_data.xlsx"'
        return response
    
    elif request.method == "POST":
        try:
            try:
                excel_file = request.FILES['excel_file']
            except:    
                raise Exception("Invalid request Excel/CSV file missing")
                
            ext = re.search(r"\.([a-zA-Z]+)$", excel_file.name).group(1)

            match ext:
                case "csv":
                    df = pd.read_csv(excel_file)
                    df['DOJ'] = pd.to_datetime(df['DOJ']).dt.date
                    
                case "xlsx":
                    df = pd.read_excel(excel_file)
                    df['DOJ'] = pd.to_datetime(df['DOJ'],unit='d').dt.date
                
                case _ :
                    #File type not supported
                    raise Exception("Invalid file type. Only '.xlsx' and '.csv' files are supported ")
            
            #Uploading file to blob to keep track
            x = datetime.datetime.now()
            uploadToBlobStorage(excel_file, f"Record/{x.year}/{excel_file.name}")
            data = df.to_dict(orient='records')
            rejected = []

            for row in data:
                record = EmployeeSerializer(data = row)
                if record.is_valid():
                    record.save()
                    pass
                else:
                    row['error'] = record.errors
                    rejected.append(row)

            result = {"Count":f"{len(data)-len(rejected)} inserted successfully out of {len(data)}",\
                      "Rejected Records":rejected}
            return Response(result, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def group(request):

    if request.method == "GET":
        g = Group.objects.all().values()
        return Response(g, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        try:
            auth_group_name = request.POST['auth_group_name']
            author_group, created = Group.objects.get_or_create(name=auth_group_name)
            permission = Permission.objects.filter(content_type=7)
            for perm in permission:
                print(perm.codename)
                author_group.permissions.add(perm)
            return Response({auth_group_name: created}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_group(request):

    try:
        auth_group_name = request.POST['auth_group_name']
        username = request.POST['username']
        user = User.objects.get(username=username)
        auth_group, created = Group.objects.get_or_create(name=auth_group_name)
        user.groups.add(auth_group)
        return Response({username: f"Added to auth group {auth_group_name}"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
def uploadToBlobStorage(file,key):
   connection_string = "DefaultEndpointsProtocol=https;AccountName=sqlvabh4mtyilkmk7w;AccountKey=Pmfzv+NUjU5u91dstc8aEy0nYSo39Bf8NUN8PJNZn9XbhXSK9lCrgEjapQRWKKmZyosv9REeLmvw+AStzH/BcA==;EndpointSuffix=core.windows.net"
   try:
        print('start')
        # blob_service_client = BlockBlobService(account_name = 'accountname', account_key='accountkey')
        # blob_service_client.create_blob_from_bytes( container_name = 'report',\
        #                                             blob_name = key,\
        #                                                   blob = file.read())
        # print('done')
        # return True
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container="report", blob=key)
        #with open(file_path,"rb") as data:
        file_content = file.read()
        data = BytesIO(file_content)
        blob_client.upload_blob(data)
        print(f"Uploaded {key}.")
   
   except Exception as e:
       print(e)
       return False