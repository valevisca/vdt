from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Design(models.Model):
    name = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    datedue = models.DateField(null=True, blank=True)
    dateanalysed = models.DateTimeField(null=True, blank=True)
    inputfile = models.FileField(upload_to='projects/input')

    # We have to put here a reference to the user. To do this, we have to use 
    # a ForeignKey which allows us to conenct a model to another.
    # This is a "one to many relationship", as one user can have many 
    # Todos, but one todo belongs to one user ONLY.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # SE_NOTE: by default Django models 'save' and 'delete' methods have a default behavious. For instance
    # deleting a model instance does not delete the associated files (I suppose in case someone wants)
    # to give the possibility to retrieve them or manage them in a different way.
    # It is possible to override this behaviour, by redefining the method in the model definition and
    # adding some action before and after.
    # Refer to https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-predefined-model-methods
    # for additional details
    def delete(self, *args, **kwargs):
        # Before calling the real 'delete' we remove the file from /media
        self.inputfile.delete()
        super().delete(*args, **kwargs)  # Call the "real" delete() method.

    



