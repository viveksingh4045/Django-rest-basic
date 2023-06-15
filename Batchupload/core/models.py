from django.db import models

# Create your models here.
class Employee(models.Model):
    Emp_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=80,blank=False)
    Age = models.IntegerField(blank=False)
    Phone_No = models.CharField(max_length=10,blank=False)
    Address = models.CharField(max_length=300, blank=False)
    DOJ = models.DateField(blank=False)

    class Meta:
        permissions = [
            ("bulk_download", "can do bulk download"),
            ("bulk_upload", "can do bulk upload"),
        ]

    def __str__(self) -> str:
        return self.Name
