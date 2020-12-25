from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Workouts(models.Model):
    #django will auto generate a primary key id.
    username = models.ForeignKey(User, on_delete=models.CASCADE) #delete workouts if user is deleted.
    date = models.DateTimeField(default=timezone.now)
    WName = models.CharField(max_length=50)

    def __str__(self):
        return self.WName
