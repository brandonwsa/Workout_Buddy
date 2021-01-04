from rest_framework import serializers
from .models import Exercises

class ExercisesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercises
        fields = ['id', 'username', 'date', 'exercise', 'sameWeight', 'totalVolume']