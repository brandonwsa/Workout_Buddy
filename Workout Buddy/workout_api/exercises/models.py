from django.db import models
from workouts.models import Workouts
from django.urls import reverse

class Exercises(models.Model):
    #django will auto generate a primary key id.
    workout_id = models.ForeignKey(Workouts, default=None, on_delete=models.CASCADE) #delete exercise if workout it is associated with is deleted.
    date = models.DateField()
    exercise = models.CharField(max_length=50)
    sameWeight = models.BooleanField(default=False)
    totalVolume = models.IntegerField(default=0) #is able to be null or blank. Will be auto filled in by after exercises details are inputted.

    def __str__(self):
        return self.exercise


    #reverse function to get url route as string
    def get_absolute_url(self):
        return reverse('exercises-detail', kwargs={'pk': self.workout_id.pk, 'exercisepk': self.pk}) #also need primary key from this exercise
