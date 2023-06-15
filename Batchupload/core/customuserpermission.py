from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission

class BatchUploadDownloadPermission(BasePermission):

    def has_permission(self, request, view):
        #print("User Permission")
        #print(request.user.get_all_permissions())
        return request.user and request.user.groups.filter(name='bulk_upload_download').exists()
    
    def has_object_permission(self, request, view, obj):
        print("Object Permission")
        print(view, obj)
        return super().has_object_permission(request, view, obj)