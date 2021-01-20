from rest_framework import serializers
from .models import Exercises
from workouts.serializers import WorkoutsSerializer

class ExercisesSerializer(serializers.HyperlinkedModelSerializer):

    #uses workouts serializer for workout_id to display the workout assocaited with this details in the JSON.
    workout_id = WorkoutsSerializer(read_only=True)

    class Meta:
        model = Exercises
        fields = ['id', 'workout_id', 'date', 'exercise', 'sameWeight', 'totalVolume']