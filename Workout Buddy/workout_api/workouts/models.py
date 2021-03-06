from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Workouts(models.Model):
    #django will auto generate a primary key id.
    username = models.ForeignKey(User, on_delete=models.CASCADE) #delete workouts if user is deleted.
    date = models.DateField()
    WName = models.CharField(max_length=50)

    def __str__(self):
        return self.WName


    #reverse function to get url route as string
    def get_absolute_url(self):
        return reverse('workouts-detail', kwargs={'pk': self.pk}) #also need primary key from this workout