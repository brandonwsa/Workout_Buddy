from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Exercises(models.Model):
    #django will auto generate a primary key id.
    username = models.ForeignKey(User, on_delete=models.CASCADE) #delete workouts if user is deleted.
    date = models.DateField()
    exercise = models.CharField(max_length=50)
    sameWeight = models.BooleanField(default=False)
    totalVolume = models.IntegerField(null=True, blank=True) #is able to be null or blank. Will be auto filled in by after exercises details are inputted.

    def __str__(self):
        return self.exercise


    #reverse function to get url route as string
    def get_absolute_url(self):
        return reverse('exercises-detail', kwargs={'pk': self.pk}) #also need primary key from this workout
