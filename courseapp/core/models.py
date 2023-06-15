from django.db import models

# Create your models here.
class Course(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=300)
    rating = models.DecimalField(max_digits=2,decimal_places=1)

    def __str__(self) -> str:
        return self.name