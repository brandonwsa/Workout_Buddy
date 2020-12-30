from rest_framework import serializers
from .models import Workouts

class WorkoutsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Workouts
        fields = ['id', 'username', 'date', 'WName']