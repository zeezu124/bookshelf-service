from django.db import models
from djongo import models as djmodels

# Create your models here.
class Book(models.Model):
    book_id = models.CharField(primary_key=True, 
                               max_length=50)

class Library(models.Model):
    id = models.IntegerField()
    username = models.CharField(primary_key=True,
                                max_length=50)
    book_ids = djmodels.ArrayField(model_container= Book)