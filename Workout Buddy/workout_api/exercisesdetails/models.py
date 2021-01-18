from django.db import models
from exercises.models import Exercises
from django.urls import reverse

class ExercisesDetails(models.Model):
    #django will auto generate a primary key id.
    exercise_id = models.ForeignKey(Exercises, default=None, on_delete=models.CASCADE) #delete exercise details if exercise it is associated with is deleted.
    weight = models.IntegerField()
    set_amount = models.IntegerField()
    total_reps = models.IntegerField()
    volume = models.IntegerField(default=0) #is able to be null or blank. Will be auto filled in by after exercises details are inputted.
                                                        #need to make default: 0

    def __str__(self):
        return self.exercise_id.exercise


    #reverse function to get url route as string
    def get_absolute_url(self):
        return reverse('exercisesdetails-detail', kwargs={'pk': self.exercise_id.workout_id.pk, 'exercisepk': self.exercise_id.pk, 'exercisedetailpk': self.pk}) #also need primary key from this exercise_details
