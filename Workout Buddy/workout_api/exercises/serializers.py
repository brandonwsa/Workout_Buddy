from rest_framework import serializers
from .models import Exercises

class ExercisesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercises
        fields = ['id', 'workout_id', 'date', 'exercise', 'sameWeight', 'totalVolume']